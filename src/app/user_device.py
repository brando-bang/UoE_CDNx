import os
import time
from urllib.parse import quote_plus

import requests
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request

app = Flask(__name__)

ASSET_KEY = os.getenv("ndnx_asset_key").encode("utf-8")
CDN_URL = os.getenv("ndnx_qa_cdn_url")
CONTENT_KEY = os.getenv("ndnx_content_key").encode("utf-8")
NDNX_CONTENT_CACHE = os.getenv("ndnx_qa_content_cache")
QA_KEY = os.getenv("ndnx_qa_key").encode("utf-8")

asset_crypto_util = Fernet(ASSET_KEY)
content_key_crypto_util = Fernet(CONTENT_KEY)
vpn_crypto_util = Fernet(QA_KEY)


@app.route("/heartbeat")
def heartbeat():
    """Return a simple OK message for health checks."""
    return jsonify({"status": "ok", "message": "Flask heartbeat OK"}), 200


@app.route("/download_direct")
def download_direct():
    target_url = "https://mirror.nforce.com/pub/speedtests/10mb.bin"
    start_time = time.time()

    get(target_url)
    elapsed_time = time.time() - start_time

    return jsonify(str(elapsed_time * 1000) + " milliseconds")


@app.route("/download_cdn")
def download_cdn():
    start_time = time.time()

    get(CDN_URL + "10mb.bin")
    elapsed_time = time.time() - start_time

    return jsonify(str(elapsed_time * 1000) + " milliseconds")


@app.route("/use_vpn")
def send_request():
    try:
        start_time = time.time()

        target_url = request.args.get("url")
        target_endpoint = request.args.get("endpoint")
        plaintext_vpn_payload_bytes = target_endpoint.encode("utf-8")
        encrypted_vpn_payload_bytes = vpn_crypto_util.encrypt(
            plaintext_vpn_payload_bytes
        )
        encrypted_vpn_payload = encrypted_vpn_payload_bytes.decode("utf-8")
        vpn_url = target_url + "/use_vpn?vpn_payload=" + encrypted_vpn_payload

        response = requests.get(vpn_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        encrypted_vpn_response_bytes = response.content
        decrypted_vpn_response_bytes = vpn_crypto_util.decrypt(
            encrypted_vpn_response_bytes
        )
        decrypted_vpn_response_bytes.decode("utf-8")

        elapsed_time = time.time() - start_time

        return jsonify(str(elapsed_time * 1000) + " milliseconds")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/use_ndnx")
def use_ndnx():
    try:
        start_time = time.time()
        content_key = request.args.get("content_key")
        encrypted_content_key = content_key_crypto_util.encrypt(
            content_key.encode("utf-8")
        ).decode("utf-8")

        content_key_query_param = quote_plus(encrypted_content_key)

        target_url = request.args.get("url")

        encrypted_ndnx_content_key = get(
            f"{target_url}/use_ndnx?content_key={content_key_query_param}"
        )

        ndnx_content_key = vpn_crypto_util.decrypt(encrypted_ndnx_content_key).decode(
            "utf-8"
        )

        encrypted_asset = get(CDN_URL + ndnx_content_key)

        asset_crypto_util.decrypt(encrypted_asset)

        elapsed_time = time.time() - start_time

        return jsonify(str(elapsed_time * 1000) + " milliseconds")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


def get(target_url):
    try:
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }

        response = requests.get(target_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        return response.content
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Listen on all interfaces, port 8000
    app.run(host="0.0.0.0", port=8000)
