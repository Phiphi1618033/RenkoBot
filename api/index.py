import json
import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")


def send_telegram_message(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        },
        timeout=15
    )

    return response.json()


def handler(request):

    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({
                "error": "Method Not Allowed"
            })
        }

    try:

        payload = request.get_json()

        if payload.get("secret") != WEBHOOK_SECRET:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "error": "Forbidden"
                })
            }

        symbol = payload.get("symbol", "")
        side = payload.get("side", "")
        entry = payload.get("entry", "")
        sl = payload.get("sl", "")
        tp = payload.get("tp", "")
        timeframe = payload.get("timeframe", "")

        telegram_message = (
            f"🚨 {side} SIGNAL\n\n"
            f"Pair: {symbol}\n"
            f"Timeframe: {timeframe}\n\n"
            f"Entry: {entry}\n"
            f"Stop Loss: {sl}\n"
            f"Take Profit: {tp}"
        )

        send_telegram_message(telegram_message)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success"
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }
