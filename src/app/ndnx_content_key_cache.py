from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/heartbeat")
def heartbeat():
    """Return a simple OK message for health checks."""
    return jsonify({"status": "ok", "message": "Flask heartbeat OK"}), 200


@app.route("/content_key")
def check_content_key():
    content_key = request.args.get("content_key")

    if content_key == "10mb.bin":
        return "gAAAAABpNfPVKq01kUouFVsT2PQGo83UWEuWevxB9TjVEz2D1v9Pz2y18QZtohsCpEhHP0GQ6sUYB1Bzcp4-_0akVGeMPLhd4g=="

    return jsonify("Key not found", 500)


if __name__ == "__main__":
    # Listen on all interfaces, port 8000
    app.run(host="0.0.0.0", port=8000)
