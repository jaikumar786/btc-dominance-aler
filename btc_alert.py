import requests
import time
from telegram import Bot

# Telegram bot credentials
TELEGRAM_BOT_TOKEN = "7711350576:AAH8fpf9mPkAPgs2Y0pyr1CP4GvwVqD8FyM"
TELEGRAM_CHAT_ID = "7930747912"

# API for BTC Dominance
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/global"

# Tracking BTC dominance
last_dominance = None

# Function to get BTC dominance
def get_btc_dominance():
    try:
        response = requests.get(COINGECKO_API_URL)
        data = response.json()
        return data["data"]["market_cap_percentage"]["btc"]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to send Telegram alert
def send_telegram_alert(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Monitor BTC dominance
while True:
    current_dominance = get_btc_dominance()
    
    if current_dominance is not None:
        global last_dominance
        if last_dominance is not None and abs(current_dominance - last_dominance) >= 0.10:
            message = f"⚠️ BTC Dominance Alert: {current_dominance}% (Change: {current_dominance - last_dominance:.2f}%)"
            send_telegram_alert(message)
        
        last_dominance = current_dominance
    
    # Check every 5 minutes
    time.sleep(300)