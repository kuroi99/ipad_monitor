import time
import json
import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()


KEYWORD = "第3世代"

url = "https://www.apple.com/jp/shop/refurbished/ipad"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_notification(title, message):
    os.system("afplay /System/Library/Sounds/Submarine.aiff")
    print(f"【発見】 {message}")
    
    # メール設定
    GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    TO_ADDRESS = os.getenv("TO_ADDRESS")    

    msg = MIMEText(message)
    msg["Subject"] = title
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = TO_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

SEEN_FILE = "seen_products.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
           return json.load(f)
    return []

def save_seen(products):
    with open(SEEN_FILE, "w") as f:
        json.dump(products, f)

while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("h3")
    found_any = False
    seen = load_seen()
    new_products = []

    print("---検索開始---")
    for product in products:
        link = product.find("a", href=lambda h: h and "/jp/shop/product" in h)
        if not link:
            continue
        name = product.get_text().strip()

        price_tag = product.find_next("div", class_="as-price-currentprice")
        price = price_tag.get_text().strip() if price_tag else "価格不明"

        if "iPad Air" in name or ("iPad Pro" in name and KEYWORD in name):
            if name not in seen:
                print(f"*新着ヒット!!: {name} / {price}")
                send_notification("iPad入荷!", f"{name} / {price}")
                found_any = True
            new_products.append(name)
        else:
            print(f"対象外: {name[:20]}...")

    save_seen(new_products)


    if not found_any:
        print("現在、ターゲットの在庫はありません。")
    print("30分後に再チェックします...")
    time.sleep(1800)