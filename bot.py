import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# BOT TOKEN tuleb Railway environment variablist "TOKEN"
TOKEN = os.getenv("TOKEN")

# Sinu grupi link
GROUP_LINK = "https://t.me/+tZVb6VQnMrk4MGQ0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "Welcome to DoggieMarket! 🐶🛒\n\n"
        f"Join here: {GROUP_LINK}"
    )

    # Saadame pildi failist doggie.jpg
    with open("doggie.jpg", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("Bot töötab!")
    app.run_polling()
    

