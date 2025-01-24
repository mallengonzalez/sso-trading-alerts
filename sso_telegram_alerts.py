import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Telegram credentials (loaded from GitHub Secrets)
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def send_telegram_alert(message):
    """Send message via Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

def check_signals():
    # Inside check_signals():
    print("Latest SSO Price:", latest['price'])
    print("Latest RSI:", latest['rsi'])
    print("Latest VIX:", latest['vix'])
    print("EMA Crossover:", latest['ema_cross'])

    message = "🚀 TEST ALERT: GitHub Actions is working!"
    send_telegram_alert(message)
#     """Check SSO buy/sell conditions"""
#     # Fetch data
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=365)
#     sso = yf.download('SSO', start=start_date, end=end_date)
#     spy = yf.download('SPY', start=start_date, end=end_date)
#     vix = yf.download('^VIX', start=start_date, end=end_date)

#     # Calculate indicators
#     spy['50_EMA'] = spy['Close'].ewm(span=50, adjust=False).mean()
#     spy['200_EMA'] = spy['Close'].ewm(span=200, adjust=False).mean()
#     delta = sso['Close'].diff()
#     gain = delta.where(delta > 0, 0)
#     loss = -delta.where(delta < 0, 0)
#     avg_gain = gain.rolling(14).mean()
#     avg_loss = loss.rolling(14).mean()
#     rs = avg_gain / avg_loss
#     sso['RSI'] = 100 - (100 / (1 + rs))

#     # Latest values
#     latest = {
#         'price': sso['Close'].iloc[-1],
#         'rsi': sso['RSI'].iloc[-1],
#         'vix': vix['Close'].iloc[-1],
#         'ema_cross': spy['50_EMA'].iloc[-1] > spy['200_EMA'].iloc[-1],
#         'sso_high_20': sso['High'].rolling(20).max().iloc[-1]
#     }

#     # Buy conditions
#     if (
#         latest['ema_cross'] and
#         latest['rsi'] < 35 and
#         latest['vix'] < 25 and
#         latest['price'] < 0.97 * latest['sso_high_20']
#     ):
#         message = f"""🚀 **SSO BUY SIGNAL** 🚀
# Price: ${latest['price']:.2f}
# RSI: {latest['rsi']:.1f}
# VIX: {latest['vix']:.1f}"""
#         send_telegram_alert(message)

#     # Sell conditions
#     elif latest['rsi'] > 65 or latest['vix'] > 30:
#         message = f"""⚠️ **SSO SELL SIGNAL** ⚠️
# Price: ${latest['price']:.2f}
# RSI: {latest['rsi']:.1f}
# VIX: {latest['vix']:.1f}"""
#         send_telegram_alert(message)

# if __name__ == "__main__":
#     check_signals()
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print("Telegram API Response:", response.json())  # Debug line
    return response.json()
