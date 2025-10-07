from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

Token: Final = '8151826785:AAHKNffohvCm-RD2Npz1wD4nU25LqkD9BiY'
BOT_USERNAME: Final = '@Narutosasukae_bot'

# Store user states: {chat_id: {"step": int, "name": str, "age": str}}
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user_states[chat_id] = {"step": 1}
    await update.message.reply_text('Hello! What is your name?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help message\n/about - Information about the bot')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    # If user hasn't started, prompt them to use /start
    if chat_id not in user_states:
        await update.message.reply_text('Please type /start to begin.')
        return

    state = user_states[chat_id]

    if state["step"] == 1:
        # User should reply with their name
        state["name"] = text
        state["step"] = 2
        await update.message.reply_text(f"Nice to meet you, {text}! What is your age?")
    elif state["step"] == 2:
        # User should reply with their age
        state["age"] = text
        state["step"] = 3
        await update.message.reply_text("Thank you! What is your address?")
    elif state["step"] == 3:
        # User should reply with their address
        state["address"] = text
        await update.message.reply_text(
            f"Thank you, {state['name']}!\n"
            f"Age: {state['age']}\n"
            f"Address: {state['address']}\n"
            "Your information has been recorded."
        )
        # Optionally reset or remove state
        user_states.pop(chat_id)
    else:
        await update.message.reply_text("Please type /start to begin.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(Token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_error_handler(error)

    print('Bot is running...')
    app.run_polling(poll_interval=3)
