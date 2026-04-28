import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======================
# CONFIG
# ======================
API_KEY = os.getenv("AIzaSyDEn8FDaIPbs2CrGCUv_aH8vNIG5JsLJr4")
BOT_TOKEN = os.getenv("8775759479:AAEimWzCkeOpgwEZjIS-GHPss-YlHcvy9ew")

URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"


# ======================
# GEMINI FUNCTION
# ======================
def ask_gemini(prompt: str):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(URL, json=payload, timeout=30)
        data = res.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"AI error: {e}"


# ======================
# COMMANDS
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AutoCoder Bot Online!\n\n"
        "Commands:\n"
        "/ai <prompt>\n"
        "/ping\n"
        "/help"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ai <text> - Ask AI\n"
        "/ping - test bot\n"
        "/info - bot info"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot: AutoCoder AI\n"
        "🔥 Powered by Gemini\n"
        "☁️ Hosted on Render"
    )


async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("Usage: /ai hello")
        return

    reply = ask_gemini(prompt)
    await update.message.reply_text(reply)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("ai", ai))

    print("🤖 Bot running...")
    app.run_polling(drop_pending_updates=True)
