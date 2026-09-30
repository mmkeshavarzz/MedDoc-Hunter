# =============================================================================
# * Project: Medical PDF/PPT Hunter 🩺
# * Author: mm.keshavarz | Enhanced by Senior Dev 👨‍⚕️
# * Features: Telethon Scraping, Auto Forward, Hashtag Categorization
# =============================================================================

import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename

# اطلاعات رو از گیت‌هاب سکرت می‌گیریم
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING") # باید با اسکریپت String Session بسازیش
DESTINATION_CHANNEL = os.environ.get("DEST_CHANNEL") # مثلا: -100123456789

CHANNELS = [
    "medical_notes_ir", "med_students_pdf", "anatomy_ppt" # آیدی کانال‌های هدف رو اینجا بذار
]

KEYWORDS = {
    "آناتومی": ["اناتومی", "anatomy", "استخوان"],
    "فارماکولوژی": ["فارماکو", "دارو", "pharma"],
    "فیزیولوژی": ["فیزیو", "physio"]
}

client = TelegramClient('session_name', API_ID, API_HASH)

def get_category(filename):
    name_lower = filename.lower()
    for cat, words in KEYWORDS.items():
        if any(w in name_lower for w in words):
            return cat
    return "عمومی"

async def main():
    await client.start()
    print("🕵️‍♂️ دکتر بات وارد بخش شد! در حال جستجوی فایل‌ها...")
    
    for channel in CHANNELS:
        try:
            print(f"🔍 در حال بررسی کانال: {channel}")
            # فقط پیام‌های حاوی داکیومنت رو می‌گیریم (مثلا 20 تای آخر)
            async for message in client.iter_messages(channel, limit=20, filter=InputMessagesFilterDocument):
                if message.document:
                    # پیدا کردن اسم فایل
                    filename = "Unknown"
                    for attr in message.document.attributes:
                        if isinstance(attr, DocumentAttributeFilename):
                            filename = attr.file_name
                            
                    ext = filename.split('.')[-1].lower()
                    if ext in ['pdf', 'ppt', 'pptx']:
                        cat = get_category(filename)
                        caption = f"🩺 **دسته‌بندی:** #{cat}\n📂 **فایل:** {filename}\n\n🤖 @mm_keshavarzz_bot"
                        
                        # فوروارد به کانال پرایویت (یا ارسال مجدد با کپشن جدید)
                        await client.send_file(DESTINATION_CHANNEL, message.document, caption=caption)
                        print(f"✅ فایل {filename} ارسال شد!")
                        await asyncio.sleep(2) # تلگرام مارو اسپمر نشناسه!
        except Exception as e:
            print(f"❌ ای بابا! خطای پزشکی در کانال {channel}: {e}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
