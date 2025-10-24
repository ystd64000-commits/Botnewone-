import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token
TOKEN = os.environ.get("TOKEN", "YOUR_BOT_TOKEN_HERE")

# Other main menu messages
menu_messages = {
    "new_stories": "នេះគឺ រឿងថ្មីៗ ...",
    "vip_group": "សូមចូលគ្រុប VIP របស់យើង...",
    "contact": "ទំនាក់ទំនង៖\n📞 0123456789\n📧 email@example.com",
    "fun_items": "របស់លេងថ្មីៗ ..."
}

# Stories folder
STORY_FOLDER = "stories"

# Read story content from file
def read_story_file(item_number):
    file_path = os.path.join(STORY_FOLDER, f"story1_{item_number}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "សុំទោស, រឿងនេះមិនមាននៅឡើយ។"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 អានរឿង", callback_data='menu_read')],
        [InlineKeyboardButton("🆕 រឿងថ្មីៗ", callback_data='new_stories')],
        [InlineKeyboardButton("🌟 គ្រុប VIP", callback_data='vip_group')],
        [InlineKeyboardButton("☎️ ទំនាក់ទំនង", callback_data='contact')],
        [InlineKeyboardButton("🎮 របស់លេងថ្មីៗ", callback_data='fun_items')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("សូមជ្រើសមីនុយខាងក្រោម👇", reply_markup=reply_markup)

# Generate 20-item submenu for story1
def generate_story_menu_20():
    keyboard = []
    for i in range(1, 21):
        keyboard.append([InlineKeyboardButton(f"រឿង{i}", callback_data=f'story{i}')])
    keyboard.append([InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='menu_read')])
    return InlineKeyboardMarkup(keyboard)

# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Main Menu → អានរឿង
    if query.data == 'menu_read':
        keyboard = [
            [InlineKeyboardButton("រឿង1", callback_data='story_main')],
            [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("សូមជ្រើសរើសរឿង:", reply_markup=reply_markup)
        return

    # Submenu 20 items for រឿង1
    if query.data == 'story_main':
        reply_markup = generate_story_menu_20()
        await query.edit_message_text("សូមជ្រើសរើសរឿងចំណាត់ថ្នាក់ 1-20:", reply_markup=reply_markup)
        return

    # Show story content from file
    if query.data.startswith('story'):
        item_number = int(query.data.replace('story',''))
        story_text = read_story_file(item_number)
        await query.edit_message_text(story_text)
        return

    # Other main menu options
    if query.data in menu_messages:
        await query.edit_message_text(menu_messages.get(query.data))
        return

    # Back to main menu
    if query.data == "back_main":
        await start(update, context)
        return

    await query.edit_message_text("មិនមានអត្ថបទសម្រាប់ Menu នេះ")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
