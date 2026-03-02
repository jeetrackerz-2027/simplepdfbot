import telebot
from flask import Flask, request
import json

TOKEN = "8065211538:AAGh9wELVIOK58fFklOBvy1UswEFoy7wzyo"
ADMIN_ID = 7371121826

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DATA_FILE = "data.json"

# Load data
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except:
    data = {
        "books": {},
        "users": []
    }

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in data["users"]:
        data["users"].append(user_id)
        save()

    bot.send_message(
        message.chat.id,
        "══════════════════════════════\n"
        "        🎓  𝐉𝐄𝐄 𝐓𝐑𝐀𝐂𝐊𝐄𝐑 𝐕𝐀𝐔𝐋𝐓  🎓\n"
        "══════════════════════════════\n\n"
        "📘 Official Academic Resource Portal\n\n"
        "Providing structured digital access for serious aspirants\n"
        "preparing for competitive examinations:\n\n"
        "   ▸ Joint Entrance Examination (JEE)\n"
        "   ▸ National Eligibility cum Entrance Test (NEET)\n"
        "   ▸ CBSE Board Examinations\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 Secure Access System\n"
        "⚡ Instant PDF Delivery\n"
        "📂 Organized Digital Archive\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📢 BACKUP CHANNEL\n"
        "🔗 https://t.me/JEECBSENEETBOOKS\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Excellence requires discipline."
    )

# ---------------- ADD BOOK ----------------
@bot.message_handler(content_types=['document'])
def save_book(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.caption:
        bot.reply_to(message, "⚠ Book name caption me likho.")
        return

    key = message.caption
    file_id = message.document.file_id

    data["books"][key] = file_id
    save()

    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={key}"

    bot.reply_to(
        message,
        f"✅ Book Saved!\n\n🔗 Unique Link:\n{link}"
    )

# ---------------- WEBHOOK ----------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.get_data().decode("UTF-8")
    )
    bot.process_new_updates([update])
    return "", 200

@app.route("/")
def index():
    return "Bot Running"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://jee-cbse-bot-eqpf.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
