import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading

# Initialize the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define your bot token
TOKEN = os.getenv("BOT_TOKEN")

# Telegram bot handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This is your bot.")

# Function to run the Telegram bot
async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

# Flask route
@app.route('/')
def index():
    return "Hello from Flask!"

# Function to run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start both the bot and Flask in separate threads
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
