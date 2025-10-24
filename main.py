import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "YOUR_BOT_TOKEN_HERE")

# Messages for other main menu options
menu_messages = {
    "new_stories": "នេះគឺ រឿងថ្មីៗ ...",
    "vip_group": "សូមចូលគ្រុប VIP របស់យើង...",
    "contact": "ទំនាក់ទំនង៖\n📞 0123456789\n📧 email@example.com"
}

# Stories folder
STORY_FOLDER = "stories"

# Helper function to read story file
def read_story_file(story_key, item_index):
    file_path = os.path.join(STORY_FOLDER, f"{story_key}_{item_index+1}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "សុំទោស, រឿងនេះមិនមាននៅឡើយ។"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 អានរឿង", callback_data='story_main')],
        [InlineKeyboardButton("🆕 រឿងថ្មីៗ", callback_data='new_stories')],
        [InlineKeyboardButton("🌟 គ្រុប VIP", callback_data='vip_group')],
        [InlineKeyboardButton("☎️ ទំនាក់ទំនង", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("សូមជ្រើសមីនុយខាងក្រោម👇", reply_markup=reply_markup)

# Generate submenu for each story (7 items)
def generate_story_keyboard(story_key, total_items=7, back_data='story_main'):
    keyboard = []
    for i in range(1, total_items+1):
        keyboard.append([InlineKeyboardButton(f"រឿង{i}", callback_data=f"{story_key}_{i}")])
    keyboard.append([InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data=back_data)])
    return InlineKeyboardMarkup(keyboard)

# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Main Menu → អានរឿង
    if query.data == "story_main":
        keyboard = [
            [InlineKeyboardButton("រឿង1", callback_data='story1')],
            [InlineKeyboardButton("រឿង2", callback_data='story2')],
            [InlineKeyboardButton("រឿង3", callback_data='story3')],
            [InlineKeyboardButton("រឿង4", callback_data='story4')],
            [InlineKeyboardButton("រឿង5", callback_data='story5')],
            [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("សូមជ្រើសរើសរឿងដែលអ្នកចង់អាន👇", reply_markup=reply_markup)
        return

    # Submenu for story → 7 items
    if query.data in ['story1','story2','story3','story4','story5']:
        reply_markup = generate_story_keyboard(query.data, total_items=7)
        await query.edit_message_text(f"សូមជ្រើសរើសអត្ថបទសម្រាប់ {query.data}👇", reply_markup=reply_markup)
        return

    # Show story content from files
    if "_" in query.data:
        story_key, item_index = query.data.split("_")
        item_index = int(item_index) - 1
        story_text = read_story_file(story_key, item_index)
        await query.edit_message_text(story_text)
        return

    # Other main menu options
    if query.data in ["new_stories","vip_group","contact"]:
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
