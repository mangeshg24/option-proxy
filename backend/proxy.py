from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/nse/optionchain", methods=["GET"])
def option_chain():
    symbol = request.args.get("symbol", "NIFTY")
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        session = requests.Session()
        html = session.get("https://www.nseindia.com", headers=headers)
        cookies = html.cookies
        r = session.get(url, headers=headers, cookies=cookies)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
