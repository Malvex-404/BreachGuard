from flask import Flask, render_template, request, send_file
from flask import session, redirect, url_for

# Services
from services.breach_service import detect_query
from services.risk_service import calculate_risk
from services.password_service import analyze_password
from services.reporter import generate_report

# Database

app = Flask(__name__)
app.secret_key = "dev_secret_key"


# -------------------------------
# PUBLIC LANDING PAGE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    detection = None
    risk = None
    query = None
    preview_mode = True   # Public users see limited data

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            detection = detect_query(query)
            risk = calculate_risk(detection)

    return render_template(
        "index.html",
        detection=detection,
        risk=risk,
        query=query,
        preview_mode=preview_mode
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


# -------------------------------
# LOGIN (Will connect to MySQL later)
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login_page():
    return render_template("login.html")


# -------------------------------
# REGISTER (Will connect to MySQL later)
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register_page():
    return render_template("register.html")


# -------------------------------
# DASHBOARD (Protected)
# -------------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


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


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)