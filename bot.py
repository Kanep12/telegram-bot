import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")  # Token loetakse Railway environment variable'st
LINK = "Test"  # siia pane link, mida bot saadab


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Siin on su link: {LINK}")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot töötab!")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
