from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


@app.route("/api/webhook", methods=["POST"])
def webhook():

    try:

        payload = request.get_json(force=True)

        if payload.get("secret") != WEBHOOK_SECRET:
            return jsonify({
                "status": "forbidden"
            }), 403

        symbol = payload.get("symbol", "")
        side = payload.get("side", "")
        entry = payload.get("entry", "")
        sl = payload.get("sl", "")
        tp = payload.get("tp", "")
        timeframe = payload.get("timeframe", "")

        message = (
            f"🚨 {side} SIGNAL\n\n"
            f"Pair: {symbol}\n"
            f"Timeframe: {timeframe}\n\n"
            f"Entry: {entry}\n"
            f"Stop Loss: {sl}\n"
            f"Take Profit: {tp}"
        )

        telegram_url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendMessage"
        )

        requests.post(
            telegram_url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )

        return jsonify({
            "status": "success"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
