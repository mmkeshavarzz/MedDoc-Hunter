# =============================================================================
# * Project: Medical PDF/PPT Hunter 🩺 (Ninja Version 🥷)
# * Author: mm.keshavarz | Enhanced by Senior Dev 👨‍⚕️
# * Features: Web Scraping (No API_ID), Bot API CopyMessage, Smart Categorization
# =============================================================================

import os
import time
import requests
from bs4 import BeautifulSoup

# اطلاعات رو از گیت‌هاب سکرت می‌گیریم
BOT_TOKEN = os.environ.get("BOT_TOKEN") # از بات‌فادر بگیر
DEST_CHANNEL = os.environ.get("DEST_CHANNEL") # مثلا: @MyPrivateMedChannel یا آیدی عددی

CHANNELS = [
    "ifmbkfu", "kazankay", "Russianway2024", # آیدی کانال‌های هدف بدون @

    "AtlasOfAnatomy", "tums_write1401", "medofast_balini", 
    "anatomi_akland", "dr_jozveh", "MedBuk"
]

KEYWORDS = {
    "آناتومی": ["اناتومی", "anatomy", "استخوان", "اسکلت"],
    "فارماکولوژی": ["فارماکو", "دارو", "pharma", "داروشناسی"],
    "فیزیولوژی": ["فیزیو", "physio", "عملکرد"]
}

def get_category(text):
    text_lower = text.lower()
    for cat, words in KEYWORDS.items():
        if any(w in text_lower for w in words):
            return cat
    return "عمومی 📦"

def send_to_channel(from_chat, message_id, caption):
    """استفاده از متد copyMessage برای انتقال سریع بدون دانلود"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"
    payload = {
        "chat_id": DEST_CHANNEL,
        "from_chat_id": f"@{from_chat}",
        "message_id": message_id,
        "caption": caption,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    print("🕵️‍♂️ نینجای پزشکی وارد می‌شود! در حال گشت‌زنی در وب...")
    
    for channel in CHANNELS:
        print(f"\n🔍 در حال اسکن کانال: @{channel}")
        url = f"https://t.me/s/{channel}" # جادوی اصلی اینجاست! (اضافه شدن /s/)
        
        try:
            # درخواست به صفحه وب تلگرام با هدرهای شبیه مرورگر واقعی
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # پیدا کردن تمام پیام‌ها
            messages = soup.find_all('div', class_='tgme_widget_message')
            
            for msg in messages[-1000:]: # فقط ۱۰ پیام آخر رو چک می‌کنیم که سریع باشه
                # بررسی وجود فایل (داکیومنت)
                doc_wrap = msg.find('div', class_='tgme_widget_message_document')
                if doc_wrap:
                    file_name_tag = doc_wrap.find('div', class_='tgme_widget_message_document_title')
                    file_name = file_name_tag.text if file_name_tag else "Unknown"
                    
                    ext = file_name.split('.')[-1].lower()
                    if ext in ['pdf', 'ppt', 'pptx']:
                        # استخراج شماره پیام
                        post_id_raw = msg.get('data-post') # فرمت: channel_name/1234
                        message_id = post_id_raw.split('/')[-1]
                        
                        cat = get_category(file_name)
                        caption = f"🩺 <b>دسته‌بندی:</b> #{cat}\n📂 <b>فایل:</b> {file_name}\n\n🤖 <i>@mm_keshavarzz_bot</i>"
                        
                        print(f"🎯 فایل پیدا شد: {file_name} (ID: {message_id})")
                        
                        # انتقال فایل
                        result = send_to_channel(channel, message_id, caption)
                        
                        if result.get("ok"):
                            print(f"✅ با موفقیت به پایگاه منتقل شد!")
                        else:
                            print(f"⚠️ اخطار در انتقال: {result.get('description')}")
                        
                        time.sleep(3) # برای اینکه تلگرام رباتمون رو مسدود نکنه (حفظ پرستیژ 😎)
                        
        except Exception as e:
            print(f"❌ ای داد بر من! خطای تکنیکال در کانال {channel}: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN or not DEST_CHANNEL:
        print("🛑 داداش سکرت‌های گیت‌هاب رو ست نکردی! BOT_TOKEN و DEST_CHANNEL رو نیاز دارم.")
    else:
        main()
