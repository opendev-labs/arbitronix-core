import requests
from trading_system.core.config import Config
from trading_system.core.telemetry import logger

class TelegramNotifier:
    def __init__(self):
        self.enabled = False
        self.bot_token = ""
        self.chat_id = ""
        
        # In a real setup, these come from .env
        # self.enabled = True
        # self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        # self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, text: str):
        if not self.enabled:
            return
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🤖 **ARBITRONIX NOTIFICATION**\n\n{text}",
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Telegram failed: {response.text}")
        except Exception as e:
            logger.error(f"Telegram exception: {e}")

notifier = TelegramNotifier()
