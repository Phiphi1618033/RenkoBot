import json
import os
import requests

from http.server import BaseHTTPRequestHandler


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            payload = json.loads(body)

            secret = payload.get("secret")

            if secret != WEBHOOK_SECRET:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(
                    b'{"status":"forbidden"}'
                )
                return

            symbol = payload.get("symbol", "")
            side = payload.get("side", "")
            entry = payload.get("entry", "")
            stop_loss = payload.get("sl", "")
            take_profit = payload.get("tp", "")
            timeframe = payload.get("timeframe", "")

            message = (
                f"🚨 {side} SIGNAL\n\n"
                f"Pair: {symbol}\n"
                f"Timeframe: {timeframe}\n\n"
                f"Entry: {entry}\n"
                f"Stop Loss: {stop_loss}\n"
                f"Take Profit: {take_profit}"
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

            self.send_response(200)
            self.end_headers()

            self.wfile.write(
                b'{"status":"success"}'
            )

        except Exception as e:

            self.send_response(500)
            self.end_headers()

            self.wfile.write(
                str(e).encode()
            )
