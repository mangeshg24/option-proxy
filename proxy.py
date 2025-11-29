from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

@app.route("/")
def home():
    return jsonify({"status": "NSE Proxy Live"})


@app.route("/nse/optionchain", methods=["GET"])
def option_chain():
    try:
        symbol = request.args.get("symbol", "NIFTY")

        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS)

        response = session.get(url, headers=HEADERS, timeout=10)

        # NSE sometimes sends HTML error pages; catch them
        try:
            data = response.json()
        except:
            return jsonify({"error": "NSE Blocked HTML response"}), 500

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
