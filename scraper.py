# =============================================================================
# * Project: Medical PDF/PPT Hunter 🩺 (Bulletproof Edition 🛡️)
# * Author: mm.keshavarz | Enhanced by Senior Dev 👨‍⚕️
# * Features: Web Scraping, Direct Post Link, Instant Delivery
# =============================================================================

import os
import time
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEST_CHANNEL = os.environ.get("DEST_CHANNEL")

# لیست کانال‌ها (با کامای دقیق و جدا از هم)
CHANNELS = [
    "kazankay",
    "Russianway2024",
    "AtlasOfAnatomy",
    "tums_write1401",
    "medofast_balini",
    "anatomi_akland",
    "dr_jozveh",
    "MedBuk"
]

KEYWORDS = {
    "آناتومی 🫀": ["اناتومی", "anatomy", "استخوان", "اسکلت", "عضله"],
    "فارماکولوژی 💊": ["فارماکو", "دارو", "pharma", "داروشناسی"],
    "فیزیولوژی 🧠": ["فیزیو", "physio", "عملکرد"],
    "جزوات جامع 📚": ["جزوه", "خلاصه", "نکته", "pdf", "book"]
}

def get_category(text):
    text_lower = text.lower()
    for cat, words in KEYWORDS.items():
        if any(w in text_lower for w in words):
            return cat
    return "عمومی پزشکی 🩺"

def send_message(text, reply_markup=None):
    """ارسال پیام مستقیم به کانال مقصد"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": DEST_CHANNEL,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    res = requests.post(url, json=payload)
    return res.json()

def main():
    print("🚀 شکارچی پزشکی شروع به کار کرد...")
    total_found = 0

    for channel in CHANNELS:
        print(f"\n📡 در حال رصد کانال: @{channel}")
        url = f"https://t.me/s/{channel}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            messages = soup.find_all('div', class_='tgme_widget_message')
            
            for msg in reversed(messages[-15000:]):  # بررسی ۱۵۰۰۰ پیام آخر
                doc_wrap = msg.find('div', class_='tgme_widget_message_document')
                if doc_wrap:
                    title_tag = doc_wrap.find('div', class_='tgme_widget_message_document_title')
                    extra_tag = doc_wrap.find('div', class_='tgme_widget_message_document_extra')
                    
                    file_name = title_tag.text.strip() if title_tag else "فایل ناشناس"
                    file_size = extra_tag.text.strip() if extra_tag else "نامشخص"
                    
                    ext = file_name.split('.')[-1].lower()
                    if ext in ['pdf', 'ppt', 'pptx', 'doc', 'docx']:
                        post_id_raw = msg.get('data-post')  # channel/123
                        post_link = f"https://t.me/{post_id_raw}"
                        cat = get_category(file_name)
                        
                        caption = (
                            f"🩺 <b>فایل جدید پزشکی شکار شد!</b>\n\n"
                            f"📂 <b>عنوان:</b> <code>{file_name}</code>\n"
                            f"📊 <b>حجم:</b> {file_size}\n"
                            f"🏷 <b>دسته‌بندی:</b> #{cat.replace(' ', '_')}\n"
                            f"📢 <b>منبع:</b> @{channel}\n\n"
                            f"🔗 <b>لینک مستقیم دانلود فایل:</b>\n{post_link}\n\n"
                            f"🤖 <i>کانال مرجع: @MedDocHunter</i>"
                        )
                        
                        inline_keyboard = {
                            "inline_keyboard": [
                                [{"text": "📥 دانلود و مشاهده فایل در تلگرام", "url": post_link}]
                            ]
                        }
                        
                        print(f"🎯 پیدا شد: {file_name}")
                        res = send_message(caption, inline_keyboard)
                        
                        if res.get("ok"):
                            print(f"✅ با موفقیت به کانال ارسال شد!")
                            total_found += 1
                        else:
                            print(f"⚠️ ارور در تلگرام: {res.get('description')}")
                            
                        time.sleep(2)
        except Exception as e:
            print(f"❌ خطای اسکرپ در @{channel}: {e}")

    print(f"\n🎉 عملیات تمام! مجموعاً {total_found} فایل ارسال شد.")

if __name__ == "__main__":
    main()
