from flask import Flask, render_template, request
import pandas as pd
from modules.detector import search_breaches
from modules.risk_engine import calculate_risk

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    risk = None

    if request.method == "POST":
        query = request.form.get("query")
        result = search_breaches(query)
        risk = calculate_risk(result)

    return render_template("index.html", result=result, risk=risk)

if __name__ == "__main__":
    app.run(debug=True)