import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify(message="Curbonomix API is running", hint="try /api/health")

@app.route("/api/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    # Force a stable test port unless overridden
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
