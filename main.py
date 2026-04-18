from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import random
import json
import os
from flask import Flask
from threading import Thread

# ======================
# 🔑 التوكن
# ======================
TOKEN = "8623464854:AAFtyVm5HJu-K_qJyR5qVRefwdTG-4GHnBY"

# ======================
# 🌐 تشغيل ويب بسيط (عشان 24/7 على Render)
# ======================
web = Flask("")

@web.route("/")
def home():
    return "Bot is alive 🔥"

def run_web():
    web.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# ======================
# 📜 قصائد
# ======================
poems = [
    "إذا غامرت في شرف مروم\nفلا تقنع بما دون النجوم",
    "ومن يتهيب صعود الجبال\nيعش أبد الدهر بين الحفر",
    "على قدر أهل العزم تأتي العزائم\nوتأتي على قدر الكرام المكارم"
]

# ======================
# ❤️ مفضلة
# ======================
FAV_FILE = "fav.json"

if os.path.exists(FAV_FILE):
    favs = json.load(open(FAV_FILE, "r", encoding="utf-8"))
else:
    favs = {}

def save_fav():
    json.dump(favs, open(FAV_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ======================
# 🎮 أزرار
# ======================
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 قصيدة عشوائية", callback_data="rand")],
        [InlineKeyboardButton("🧠 شعر ذكي", callback_data="ai")],
        [InlineKeyboardButton("❤️ مفضلة", callback_data="fav")]
    ])

# ======================
# 🧠 توليد شعر ذكي
# ======================
def smart_poem(word):
    templates = [
        f"يا {word} كم فيك من جمال\nيسكن القلب بلا سؤال",
        f"{word} في الروح له مكان\nوفيه حب وأمان",
        f"سلام على {word} في كل حين\nيبقى جميل رغم السنين"
    ]
    return random.choice(templates)

# ======================
# /start
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك في بوت الشعر الذكي", reply_markup=menu())

# ======================
# الأزرار
# ======================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)

    if q.data == "rand":
        poem = random.choice(poems)
        await q.message.reply_text(f"📜\n{poem}")

    elif q.data == "ai":
        await q.message.reply_text("🧠 اكتب: شعر عن (أي كلمة)")

    elif q.data == "fav":
        user = favs.get(uid, [])
        if not user:
            await q.message.reply_text("ما عندك مفضلة 😅")
        else:
            await q.message.reply_text("\n\n".join(user))

# ======================
# الرسائل
# ======================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = str(update.message.from_user.id)

    # 🧠 شعر ذكي
    if "شعر عن" in text:
        word = text.replace("شعر عن", "").strip()
        poem = smart_poem(word)

        await update.message.reply_text(f"📜\n{poem}")

        # حفظ بالمفضلة
        favs.setdefault(uid, [])
        if poem not in favs[uid]:
            favs[uid].append(poem)
            save_fav()

        return

    # 📜 بحث داخل الشعر
    for p in poems:
        if text in p:
            await update.message.reply_text(f"📜\n{p}")

            favs.setdefault(uid, [])
            if p not in favs[uid]:
                favs[uid].append(p)
                save_fav()
            return

    await update.message.reply_text("اكتب: شعر عن (أي كلمة) أو جرب الأزرار 👇")

# ======================
# 🚀 تشغيل البوت
# ======================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot is running...")
app.run_polling()
