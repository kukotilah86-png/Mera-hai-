from flask import Flask, request, jsonify, Response
import requests
from datetime import datetime

app = Flask(__name__)

# ================= KEY CONFIG =================

VALID_KEYS = ["7trial", "uuUsersXinfo_admin"]
EXPIRE_AT = datetime(2026, 11, 11, 23, 59, 59)  # Expiry Date Updated

# ================= ROUTES CONFIG =================
# replace with ur real api aur {term} remove mat karna

ROUTES = {
    "mobile": lambda term: f"",
    "

# ================= MAIN API ROUTE =================

@app.route("/api", methods=["GET"])
def proxy():
    key = request.args.get("key")
    type_ = request.args.get("type")
    term = request.args.get("term")

    # Key validation
    if key not in VALID_KEYS:
        return jsonify({
            "success": False,
            "error": "Invalid or missing key",
            "credit": "@UsersXinfo_admin"
        }), 401

    # Expiry check
    if datetime.utcnow() > EXPIRE_AT:
        return jsonify({
            "success": False,
            "error": "This proxy has expired",
            "credit": "@UsersXinfo_admin"
        }), 410

    # Parameter check
    if not type_ or not term:
        return jsonify({
            "success": False,
            "error": "Missing type or term",
            "credit": "@UsersXinfo_admin"
        }), 400

    route_fn = ROUTES.get(type_.lower())
    if not route_fn:
        return jsonify({
            "success": False,
            "error": f"Unknown type '{type_}'. Allowed: {', '.join(ROUTES.keys())}",
            "credit": "@UsersXinfo_admin"
        }), 400

    target_url = route_fn(term)

    try:
        resp = requests.get(target_url, timeout=10)

        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection"
        ]

        headers = [
            (name, value)
            for (name, value) in resp.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(resp.content, resp.status_code, headers)

    except requests.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch target URL: {str(e)}",
            "credit": "@UsersXinfo_admin"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)