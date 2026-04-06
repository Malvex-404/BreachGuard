from flask import Flask, render_template, request, send_file
from flask import session, redirect, url_for
from services.breach_service import detect_query
from services.risk_service import calculate_risk
from services.password_service import analyze_password
from services.reporter import generate_report
from database.db import get_connection
from services.auth_service import register_user
from services.auth_service import login_user
from services.monitor_service import (add_monitor_email,check_monitor_status,mark_breach_resolved, remove_monitor_email)
from services.recommendation_service import get_recommendations
from services.monitor_service import mark_breach_resolved
from services.notification_service import get_notifications, mark_notification_read
from services.notification_service import unread_notification_count
from services.breach_simulator import simulate_breaches

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

try:
    conn = get_connection()
    print("Database connected successfully")
    conn.close()
except Exception as e:
    print("Database connection failed:", e)

@app.route("/check")
def check():
    return "Routes working"
# -------------------------------
# PUBLIC LANDING PAGE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    detection = None
    preview_records = None
    is_logged_in = "user_id" in session

    if request.method == "POST":
        query = request.form.get("query")
        detection = detect_query(query)

        if detection and detection["found"]:
            if not is_logged_in:
                # Limit preview to first 2 records
                preview_records = detection["records"][:2]
            else:
                preview_records = detection["records"]

    return render_template(
        "index.html",
        detection=detection,
        records=preview_records,
        is_logged_in=is_logged_in
    )

# -------------------------------
# PASSWORD CHECK
# -------------------------------
@app.route("/password-check", methods=["GET", "POST"])
def password_check():

    result = None

    if request.method == "POST":
        password = request.form.get("password")

        if password:
            result = analyze_password(password)

    return render_template("password_check.html", result=result)



@app.route("/register", methods=["GET", "POST"])
def register():

    message = None

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password != confirm:
            message = "Passwords do not match"
        else:
            result = register_user(username, email, password)
            message = result["message"]

            if result["success"]:
                return redirect("/login")

    return render_template("register.html", message=message)


# -------------------------------
# DASHBOARD (Protected)
# -------------------------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    detection = None
    risk = None
    query = None

    # -----------------------------
    # Handle POST requests
    # -----------------------------
    if request.method == "POST":

        form_type = request.form.get("form_type")

        # Add monitored email
        if form_type == "monitor":
            monitor_email = request.form.get("monitor_email")

            if monitor_email:
                add_monitor_email(user_id, monitor_email)

        # Search breach
        elif form_type == "search":
            query = request.form.get("query")

            if query:
                detection = detect_query(query)

                if detection and detection.get("found"):
                    risk = calculate_risk(detection)

    # -----------------------------
    # Monitoring Results
    # -----------------------------
    monitor_results = check_monitor_status(user_id)

    # Determine monitoring risk status properly
    for item in monitor_results:
    
        unresolved_found = False
    
        for record in item.get("records", []):
            if not record.get("resolved"):
                unresolved_found = True
                break
            
        item["risk_status"] = "risk" if unresolved_found else "resolved"

    total_breaches = 0
    leaked_passwords = 0

    if detection and detection.get("found"):

        total_breaches = len(detection["records"])

        leaked_passwords = sum(
            1 for r in detection["records"]
            if r.get("password_status") == "Leaked"
        )

# -----------------------------
# Security Risk Score
# -----------------------------
    risk_score = 0

    for item in monitor_results:

        for record in item.get("records", []):

            # Ignore resolved breaches
            if record.get("resolved"):
                continue

            risk_score += 10

            if record.get("password_status") == "Leaked":
                risk_score += 30

    risk_score = min(risk_score, 100)
    
    # -----------------------------
    # Breach Alerts for Monitored Emails
    # -----------------------------
    breach_alerts = []
    
    for item in monitor_results:
    
        unresolved = [
            r for r in item.get("records", [])
            if not r.get("resolved")
        ]
    
        if unresolved:
            breach_alerts.append(item["email"])

    # -----------------------------
    # Notification Counter
    # -----------------------------
    notification_count = unread_notification_count(user_id)

    # -----------------------------
    # Render Dashboard
    # -----------------------------
    return render_template(
        "dashboard.html",
        username=session["username"],
        detection=detection,
        risk=risk,
        query=query,
        monitor_results=monitor_results,
        total_breaches=total_breaches,
        leaked_passwords=leaked_passwords,
        notification_count=notification_count,
        risk_score=risk_score,
        breach_alerts=breach_alerts
    )
# -------------------------------
# REPORT DOWNLOAD
# -------------------------------
@app.route("/report", methods=["POST"])
def report():

    query = request.form.get("query")

    detection = detect_query(query)
    risk = calculate_risk(detection)

    filepath = generate_report(query, detection, risk)

    return send_file(filepath, as_attachment=True)

@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        result = login_user(email, password)

        if result["success"]:
            session["user_id"] = result["user"]["id"]
            session["username"] = result["user"]["username"]
            return redirect(url_for("dashboard"))
        else:
            message = result["message"]

    return render_template("login.html", message=message)

@app.context_processor
def inject_notification_count():

    if "user_id" in session:
        count = unread_notification_count(session["user_id"])
    else:
        count = 0

    return dict(notification_count=count)



@app.route("/monitoring", methods=["GET", "POST"])
def monitoring():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":

        # Remove monitored email
        if request.form.get("remove_email"):
            remove_monitor_email(
                user_id,
                request.form.get("remove_email")
            )

        # Mark breach resolved
        elif request.form.get("email") and request.form.get("breach_name"):
            mark_breach_resolved(
                user_id,
                request.form.get("email"),
                request.form.get("breach_name"),
                request.form.get("breach_date")
            )

        # Scan Now (just reload)
        elif request.form.get("action") == "scan_now":
            monitor_results = check_monitor_status(user_id)
            emails = [item["email"] for item in monitor_results]
            simulate_breaches(user_id, emails)

        # Auto Scan
        elif request.form.get("action") == "auto_scan":
            interval = request.form.get("interval")
            session["auto_scan_interval"] = interval
            session["auto_scan_enabled"] = True

        return redirect(url_for("monitoring"))

    monitor_results = check_monitor_status(user_id)

    for item in monitor_results:
        for record in item.get("records", []):
            record["recommendations"] = get_recommendations(record)

    return render_template(
    "monitoring.html",
    monitor_results=monitor_results,
    auto_scan_interval=session.get("auto_scan_interval"),
    auto_scan_enabled=session.get("auto_scan_enabled", False)
)



@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    monitor_results = check_monitor_status(user_id)

    timeline = {}
    breach_sources = {}
    password_leaks = 0
    total_breaches = 0

    for item in monitor_results:
        for record in item.get("records", []):

            total_breaches += 1

            # Timeline
            if record.get("breach_date"):
                year = record["breach_date"][:4]
                timeline[year] = timeline.get(year, 0) + 1

            # Breach source
            breach = record["breach"]
            breach_sources[breach] = breach_sources.get(breach, 0) + 1

            # Password leaks
            if record.get("password_status") == "Leaked":
                password_leaks += 1

    return render_template(
        "analytics.html",
        timeline=timeline,
        breach_sources=breach_sources,
        password_leaks=password_leaks,
        total_breaches=total_breaches
    )


@app.route("/notifications", methods=["GET", "POST"])
def notifications():

    if "user_id" not in session:
        return redirect(url_for("login"))


    user_id = session["user_id"]

    if request.method == "POST":

        # Mark ALL
        if request.form.get("mark_all"):
            from services.notification_service import mark_all_notifications_read
            mark_all_notifications_read(user_id)

        else:
            notification_id = request.form.get("notification_id")

            if notification_id:
                mark_notification_read(int(notification_id))

        return redirect(url_for("notifications"))

    alerts = get_notifications(user_id)

    return render_template(
        "notifications.html",
        alerts=alerts
    )






@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)