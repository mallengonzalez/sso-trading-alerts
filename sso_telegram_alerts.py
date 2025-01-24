import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Telegram credentials
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def send_telegram_alert(message):
    """Send message via Telegram bot with debug logging"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        print(f"📤 Telegram API Response: {response.json()}", flush=True)
        return response.json()
    except Exception as e:
        print(f"🚨 Telegram Error: {str(e)}", flush=True)
        raise

def check_signals():
    """Check SSO buy/sell conditions with debug logging"""
    try:
        print("🔄 Starting signal check...", flush=True)
        
        # Fetch data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        print(f"📅 Fetching data from {start_date.date()} to {end_date.date()}", flush=True)
        
        sso = yf.download('SSO', start=start_date, end=end_date)
        spy = yf.download('SPY', start=start_date, end=end_date)
        vix = yf.download('^VIX', start=start_date, end=end_date)
        
        # Check if data is empty
        if sso.empty or spy.empty or vix.empty:
            print("⚠️ No data found for today!", flush=True)
            return

        # Calculate indicators
        print("🧮 Calculating indicators...", flush=True)
        spy['50_EMA'] = spy['Close'].ewm(span=50, adjust=False).mean()
        spy['200_EMA'] = spy['Close'].ewm(span=200, adjust=False).mean()
        
        delta = sso['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        sso['RSI'] = 100 - (100 / (1 + rs))

        # Get latest values
        latest = {
            'price': sso['Close'].iloc[-1],
            'rsi': sso['RSI'].iloc[-1],
            'vix': vix['Close'].iloc[-1],
            'ema_cross': spy['50_EMA'].iloc[-1] > spy['200_EMA'].iloc[-1],
            'sso_high_20': sso['High'].rolling(20).max().iloc[-1]
        }

        # Debug prints
        print("\n=== MARKET DATA ===", flush=True)
        print(f"SSO Price: ${latest['price']:.2f}", flush=True)
        print(f"RSI(14): {latest['rsi']:.1f}", flush=True)
        print(f"VIX: {latest['vix']:.1f}", flush=True)
        print(f"EMA Crossover (50 > 200): {latest['ema_cross']}", flush=True)
        print(f"20-Day High: ${latest['sso_high_20']:.2f}", flush=True)
        print(f"Price < 97% of High: {latest['price'] < 0.97 * latest['sso_high_20']}\n", flush=True)

        # Buy conditions
        if (
            latest['ema_cross'] and
            latest['rsi'] < 35 and
            latest['vix'] < 25 and
            latest['price'] < 0.97 * latest['sso_high_20']
        ):
            message = f"""🚀 **SSO BUY SIGNAL** 🚀
Price: ${latest['price']:.2f}
RSI: {latest['rsi']:.1f}
VIX: {latest['vix']:.1f}"""
            print("✅ Buy conditions met! Sending alert...", flush=True)
            send_telegram_alert(message)

        # Sell conditions
        elif latest['rsi'] > 65 or latest['vix'] > 30:
            message = f"""⚠️ **SSO SELL SIGNAL** ⚠️
Price: ${latest['price']:.2f}
RSI: {latest['rsi']:.1f}
VIX: {latest['vix']:.1f}"""
            print("✅ Sell conditions met! Sending alert...", flush=True)
            send_telegram_alert(message)
        else:
            print("❌ No buy/sell conditions met today", flush=True)

    except Exception as e:
        print(f"🔥 Critical Error: {str(e)}", flush=True)
        raise

if __name__ == "__main__":
    print("\n" + "="*40, flush=True)
    print("⚡ SSO TRADING BOT STARTED ⚡", flush=True)
    check_signals()
    print("="*40 + "\n", flush=True)
