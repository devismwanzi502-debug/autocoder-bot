import os
import subprocess
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# =======================
# CONFIG
# =======================
TOKEN = "8775759479:AAEimWzCkeOpgwEZjIS-GHPss-YlHcvy9ew"
GEMINI_API_KEY = "AIzaSyC0CepxjzQEQWqcvafKnSNlhis0ibHych4"

BASE_DIR = os.path.join(os.getcwd(), "projects")

# =======================
# GEMINI AI (FIXED)
# =======================
def gemini_ai(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        r = requests.post(url, json=payload)
        data = r.json()

        if "candidates" not in data:
            return f"Gemini API error: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"AI error: {e}"# =======================
# PROJECT SYSTEM
# =======================
def create_project(name):
    path = os.path.join(BASE_DIR, name)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "app.py")

    code = f"""
print("🚀 Project {name} running")

while True:
    cmd = input("> ")
    if cmd == "exit":
        break
    print("You said:", cmd)
"""

    with open(file_path, "w") as f:
        f.write(code)

    return f"Project '{name}' created."

def run_project(name):
    path = os.path.join(BASE_DIR, name, "app.py")

    if not os.path.exists(path):
        return "Project not found."

    subprocess.Popen(["python3", path])
    return f"Running {name}..."

def list_projects():
    if not os.path.exists(BASE_DIR):
        return "No projects found."

    return "\n".join(os.listdir(BASE_DIR))

# =======================
# HANDLER
# =======================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    # CREATE
    if text.startswith("/create"):
        parts = text.split(" ", 1)
        if len(parts) < 2:
            await update.message.reply_text("Usage: /create name")
            return
        msg = create_project(parts[1])
        await update.message.reply_text(msg)
        return

    # RUN
    elif text.startswith("/run"):
        parts = text.split(" ", 1)
        if len(parts) < 2:
            await update.message.reply_text("Usage: /run name")
            return
        msg = run_project(parts[1])
        await update.message.reply_text(msg)
        return

    # LIST
    elif text.startswith("/list"):
        msg = list_projects()
        await update.message.reply_text(msg)
        return

    # AI
    elif text.startswith("/ai"):
        prompt = text.replace("/ai", "", 1).strip()
        if not prompt:
            await update.message.reply_text("Usage: /ai prompt")
            return
        reply = gemini_ai(prompt)
        await update.message.reply_text(reply)
        return

    # DEFAULT
    await update.message.reply_text(
        "Commands:\n/create name\n/run name\n/list\n/ai prompt"
    )

# =======================
# START BOT
# =======================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle))

print("🤖 AutoCoder AI Bot running...")
app.run_polling()
