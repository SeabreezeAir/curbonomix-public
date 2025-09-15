from flask import Flask, request, jsonify, send_file
from backend.quote_adapter import calculate_price, score_complexity, estimate_labor
from backend.install_notes_generator import generate_notes
from backend.bundle_adapter_packet import bundle_packet
import os

app = Flask(__name__)

@app.route("/quote", methods=["POST"])
def quote():
    data = request.json
    spec = type("Spec", (), data)()

    quote = {
        "model": spec.model,
        "price": calculate_price(spec),
        "complexity": score_complexity(spec),
        "labor_hours": estimate_labor(spec),
        "powered_by": "CURBONOMIX"
    }

    # Generate install packet
    zip_path = bundle_packet(spec)
    generate_notes(spec)

    return jsonify({
        "quote": quote,
        "download_url": f"/download/{spec.model}.zip"
    })

@app.route("/download/<model>.zip", methods=["GET"])
def download(model):
    zip_path = f"C:/Curbonomix/curbonomix-public/exports/packets/{model}.zip"
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return jsonify({"error": "Packet not found"}), 404

if __name__ == "__main__":
    app.run(port=5050)
