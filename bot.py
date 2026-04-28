import os
import logging
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- ENV ----------------
BOT_TOKEN = os.getenv("8615828077:AAFClxX-_JAqi7nl0dq1vYVhO6Z_4Bu_3b8")
GEMINI_API_KEY = os.getenv("AIzaSyDEn8FDaIPbs2CrGCUv_aH8vNIG5JsLJr4")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN missing in environment variables")

# ---------------- MEMORY ----------------
memory = {}

# ---------------- AI FUNCTION ----------------
def ask_ai(prompt: str):
    if not GEMINI_API_KEY:
        return "⚠️ AI key not set."

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        res = requests.post(url, json=payload, timeout=15)
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "⚠️ AI error occurred."

# ---------------- MENU ----------------
def menu_ui():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Chat AI", callback_data="chat")],
        [InlineKeyboardButton("🏓 Ping", callback_data="ping")],
        [InlineKeyboardButton("🧹 Clear Chat", callback_data="clear")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ])

# ---------------- COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Nova AI Bot\nUse /menu to begin."
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Main Menu:",
        reply_markup=menu_ui()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n"
        "/menu - Open menu\n"
        "/ask <text> - Ask AI directly\n"
        "/ping - Check bot\n"
        "/clear - Reset chat"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Online & Running!")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    memory[user_id] = []
    await update.message.reply_text("🧹 Chat cleared!")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("⚠️ Use: /ask what is AI?")
        return

    reply = ask_ai(text)
    await update.message.reply_text(reply)

# ---------------- BUTTON HANDLER ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    memory.setdefault(user_id, [])

    if data == "chat":
        await query.message.reply_text("💬 Just type your message.")
    
    elif data == "ping":
        await query.message.reply_text("🏓 Bot is alive!")

    elif data == "clear":
        memory[user_id] = []
        await query.message.reply_text("🧹 Cleared!")

    elif data == "help":
        await query.message.reply_text("/menu /ask /ping /clear")

# ---------------- CHAT ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    memory.setdefault(user_id, []).append(text)

    reply = ask_ai(text)
    await update.message.reply_text(reply)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("ask", ask))

    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🚀 Nova AI Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
