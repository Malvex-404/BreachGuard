from flask import Flask, render_template, request, send_file
from modules.detector import detect_query
from modules.risk_engine import calculate_risk
from modules.monitor import save_scan, load_history
from modules.reporter import generate_report
from modules.password_analyzer import analyze_password

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    detection = None
    risk = None
    query = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            detection = detect_query(query)
            risk = calculate_risk(detection)

            # Save scan to history
            save_scan(query, detection, risk)

    return render_template(
        "index.html",
        detection=detection,
        risk=risk,
        query=query
    )


@app.route("/report", methods=["POST"])
def report():
    query = request.form.get("query")

    detection = detect_query(query)
    risk = calculate_risk(detection)

    filepath = generate_report(query, detection, risk)

    return send_file(filepath, as_attachment=True)


@app.route("/history")
def history():
    history_data = load_history()
    return render_template("history.html", history=history_data)

@app.route("/password-check", methods=["GET", "POST"])
def password_check():

    result = None

    if request.method == "POST":
        password = request.form.get("password")

        result = analyze_password(password)

    return render_template("password_check.html", result=result)
if __name__ == "__main__":
    app.run(debug=True)