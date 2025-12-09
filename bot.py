import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# BOT TOKEN keskkonnamuutujast
TOKEN = os.getenv("TOKEN")

# ADMIN USER ID (SINA)
ADMIN_ID = 7936569231 

# Salvestame admini saadetud sõnumi, mida hiljem gruppi saata
pending_messages = {}

# -----------------------------
#  Sinu VANA KOOD - ALLES JÄETUD
# -----------------------------
GROUP_LINK = "https://t.me/+tZVb6VQnMrk4MGQ0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "Welcome to DoggieMarket! 🐶🛒\n\n"
        f"Join here: {GROUP_LINK}"
    )

    # saadame pildi failist
    with open("doggie.jpg", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption)



# -----------------------------
#   UUS FUNKTSIOON: ADMIN saadab sõnumi → bot küsib gruppi
# -----------------------------
async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Ainult sina saad seda funktsiooni kasutada
    if user_id != ADMIN_ID:
        return  # ignoreerib teisi

    text = update.message.text
    pending_messages[user_id] = text

    # leiame grupid, kus bot sees on
    chats = context.application.chat_data
    keyboard = []

    for chat_id, data in chats.items():
        title = data.get("title")
        # ainult grupid (-100...)
        if title and str(chat_id).startswith("-100"):
            keyboard.append(
                [InlineKeyboardButton(title, callback_data=f"send|{chat_id}")]
            )

    if not keyboard:
        return await update.message.reply_text("Bot ei ole üheski grupis.")

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Vali grupp, kuhu see sõnum saata:", reply_markup=reply_markup)



# -----------------------------
#  Kui admin valib grupi nupu
# -----------------------------
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_id != ADMIN_ID:
        return await query.edit_message_text("Sul pole luba seda kasutada.")

    data = query.data
    if data.startswith("send|"):
        chat_id = int(data.split("|")[1])
        msg = pending_messages.get(user_id)

        if not msg:
            return await query.edit_message_text("Pole sõnumit, mida saata.")

        # saadame sõnumi gruppi
        await context.bot.send_message(chat_id=chat_id, text=msg)

        await query.edit_message_text("Sõnum saadetud gruppi!")
        pending_messages.pop(user_id, None)



# -----------------------------
#  BOTI KÄIVITAMINE
# -----------------------------
app = ApplicationBuilder().token(TOKEN).build()

# vana kood
app.add_handler(CommandHandler("start", start))

# uus admin-sõnumite funktsioon
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_message))

# inline menüü
app.add_handler(CallbackQueryHandler(menu_callback))

if __name__ == "__main__":
    print("Bot töötab!")
    app.run_polling()
