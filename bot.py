import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
    filters
)

TOKEN = os.getenv("TOKEN")

ADMIN_ID = 7936569231

pending_messages = {}
known_groups = {}  # salvestame grupid siia


# -----------------------------
#  SALVESTA GRUPP, KUS BOT NÄEB UPDATE'I
# -----------------------------
async def track_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        known_groups[chat.id] = chat.title


# -----------------------------
#  SINU VANA /start (alles jäetud)
# -----------------------------
GROUP_LINK = "https://t.me/+tZVb6VQnMrk4MGQ0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "Welcome to DoggieMarket! 🐶🛒\n\n"
        f"Join here: {GROUP_LINK}"
    )

    with open("doggie.jpg", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption)


# -----------------------------
#  ADMIN SAADAB SÕNUMI → BOT ANNAB GRUPPIDE MENÜÜ
# -----------------------------
async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        return  # ignore other people

    text = update.message.text
    pending_messages[user_id] = text

    if not known_groups:
        return await update.message.reply_text("Bot ei tea veel ühtegi gruppi. Kirjuta gruppides midagi, kus bot sees on.")

    keyboard = [
        [InlineKeyboardButton(title, callback_data=f"send|{chat_id}")]
        for chat_id, title in known_groups.items()
    ]

    await update.message.reply_text(
        "Vali grupp, kuhu see sõnum saata:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -----------------------------
#  CALLBACK: ADMIN VALIB GRUPI
# -----------------------------
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return await query.edit_message_text("Sul pole luba seda kasutada.")

    data = query.data

    if data.startswith("send|"):
        chat_id = int(data.split("|")[1])
        msg = pending_messages.get(ADMIN_ID)

        if not msg:
            return await query.edit_message_text("Pole sõnumit, mida saata.")

        await context.bot.send_message(chat_id=chat_id, text=msg)

        await query.edit_message_text("Sõnum saadetud!")
        pending_messages.pop(ADMIN_ID, None)


# -----------------------------
#  BOTI KÄIVITUS
# -----------------------------
app = ApplicationBuilder().token(TOKEN).build()

# jälgi gruppe (kõik sõnumid gruppidest)
app.add_handler(MessageHandler(filters.ALL, track_groups))

# sinu vana /start
app.add_handler(CommandHandler("start", start))

# admini sõnumid
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_message))

# inline menüü
app.add_handler(CallbackQueryHandler(menu_callback))

if __name__ == "__main__":
    print("Bot töötab!")
    app.run_polling()
