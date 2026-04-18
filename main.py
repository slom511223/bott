from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8623464854:AAFtyVm5HJu-K_qJyR5qVRefwdTG-4GHnBY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت شغال 100% 🔥")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot started...")
    app.run_polling()

if nif __name__ == "__main__":
    main()
