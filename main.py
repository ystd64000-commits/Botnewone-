import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE"  # ដាក់ Token របស់អ្នកទីនេះ
bot = telebot.TeleBot(BOT_TOKEN)

STORY_FOLDER = "stories"  # Folder រក្សារឿង

def read_story_file(filename):
    path = os.path.join(STORY_FOLDER, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "⚠️ មិនឃើញ File រឿងទេ!"

def main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📖 អានរឿង", callback_data="read_story"))
    markup.add(InlineKeyboardButton("🆕 រឿងថ្មីៗ", callback_data="new_story"))
    markup.add(InlineKeyboardButton("🌟 គ្រុប VIP", callback_data="vip"))
    markup.add(InlineKeyboardButton("☎️ ទំនាក់ទំនង", callback_data="contact"))
    markup.add(InlineKeyboardButton("🎮 របស់លេងថ្មីៗ", callback_data="tools"))
    bot.send_message(chat_id, "✅ ជ្រើស Menu 👇", reply_markup=markup)

def story_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📚 រឿង1", callback_data="story1"))
    markup.add(InlineKeyboardButton("⬅️ ត្រឡប់", callback_data="back"))
    bot.send_message(chat_id, "📚 សូមជ្រើសរើសរឿង👇", reply_markup=markup)

def story1_menu(chat_id):
    markup = InlineKeyboardMarkup()
    for i in range(1, 21):
        markup.add(InlineKeyboardButton(f"រឿង{i}", callback_data=f"story1_{i}"))
    markup.add(InlineKeyboardButton("⬅️ ត្រឡប់", callback_data="read_story"))
    bot.send_message(chat_id, "📌 ជ្រើសចំណងជើងរឿង👇", reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    chat_id = call.message.chat.id

    if data == "back":
        main_menu(chat_id)
    elif data == "read_story":
        story_menu(chat_id)
    elif data == "story1":
        story1_menu(chat_id)
    elif data.startswith("story1_"):
        num = data.split("_")[1]
        content = read_story_file(f"story1_{num}.txt")
        bot.send_message(chat_id, content)

    elif data == "new_story":
        bot.send_message(chat_id, "🆕 កំពុង Update...")
    elif data == "vip":
        bot.send_message(chat_id, "🌟 VIP Coming Soon...")
    elif data == "contact":
        bot.send_message(chat_id, "☎️ Telegram: @YourContact")
    elif data == "tools":
        bot.send_message(chat_id, "🎮 របស់លេងថ្មីៗ Shedding soon...")

print("✅ Bot Running ✅")
bot.polling(non_stop=True)
