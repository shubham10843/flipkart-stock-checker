import requests
import time
import os
from flask import Flask
from threading import Thread

# ===== TELEGRAM CONFIG FROM RENDER ENV =====
BOT_TOKEN = os.environ.get("8799365492:AAHKddVToj54YnNmwB23Ww3m0SrYJqIpae4")
CHAT_ID = os.environ.get("5954672110")

# ===== PRODUCTS =====
PRODUCTS = {
    "Casio off-white": "https://www.flipkart.com/casio-w-218hc-8avdf-youth-digital-watch-men-women/p/itm709e6e80a490e?pid=WATGGYRQJTHENBDB",
    "Casio Grey": "https://www.flipkart.com/casio-w-218h-8bvdf-youth-digital-watch-men-women/p/itm7db3694ef0fd2?pid=WATHD2RGGE6M5PH3",
    "Casio Green": "https://www.flipkart.com/casio-w-218h-3bvdf-youth-digital-watch-men-women/p/itma0055befc8a6e?pid=WATHD2RG62SGMFTC",
    "Casio Enticer": "https://www.flipkart.com/casio-mtp-1302ds-1avdf-enticer-men-analog-watch/p/itmce100b2bc44b8?pid=WATHGXZJPAFYNHZN"
}

CHECK_INTERVAL = 90  # safer interval

# ===== FLASK APP =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Stock checker running!"

# ===== TELEGRAM FUNCTION =====
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# ===== STOCK CHECK =====
def check_stock(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)

    if "BUY NOW" in response.text or "Add to cart" in response.text:
        return True
    return False

# ===== BACKGROUND LOOP =====
def stock_loop():
    already_notified = set()

    while True:
        for name, url in PRODUCTS.items():
            try:
                if check_stock(url):
                    if name not in already_notified:
                        message = f"🔥 {name} is BACK IN STOCK!\n{url}"
                        send_telegram_message(message)
                        already_notified.add(name)
                else:
                    if name in already_notified:
                        already_notified.remove(name)

            except Exception as e:
                print(f"Error checking {name}: {e}")

            time.sleep(10)  # small delay between products

        time.sleep(CHECK_INTERVAL)

# ===== START =====
def run_background():
    thread = Thread(target=stock_loop)
    thread.start()

if __name__ == "__main__":
    run_background()
    app.run(host="0.0.0.0", port=10000)