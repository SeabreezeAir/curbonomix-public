import os
import sys
from flask import Flask, request, jsonify

# ✅ Absolute path patch to recognize backend
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.quote_adapter import calculate_price, score_complexity, estimate_labor
from backend.adapter_specs_db import list_all
from backend.bundle_adapter_packet import bundle_packet
from backend.license_checker import is_valid_license

app = Flask(__name__)

@app.route("/quote", methods=["POST"])
def quote():
    spec = request.get_json()
    if not spec:
        return jsonify({"error": "Missing spec"}), 400

    license_key = spec.get("license_key")
    if not is_valid_license(license_key):
        return jsonify({"error": "Invalid or missing license key"}), 403

    price = calculate_price(spec)
    complexity = score_complexity(spec)
    labor = estimate_labor(spec)
    zip_path = bundle_packet(spec)

    return jsonify({
        "model": spec["model"],
        "price": price,
        "complexity": complexity,
        "labor_hours": labor,
        "packet_zip": zip_path
    })

if __name__ == "__main__":
    app.run(port=5050)
