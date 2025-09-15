from flask import Flask, render_template, jsonify
from backend.quote_adapter import quote_all
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/quotes")
def quotes_api():
    quotes = quote_all()
    return jsonify(quotes)

@app.route("/api/stats")
def stats():
    quotes = quote_all()
    total = len(quotes)
    avg_price = round(sum(q["price"] for q in quotes) / total, 2)
    avg_complexity = round(sum(q["complexity"] for q in quotes) / total, 2)
    avg_labor = round(sum(q["labor_hours"] for q in quotes) / total, 2)
    return jsonify({
        "total_models": total,
        "average_price": avg_price,
        "average_complexity": avg_complexity,
        "average_labor_hours": avg_labor,
        "powered_by": "CURBONOMIX"
    })

if __name__ == "__main__":
    app.run(port=5051)
