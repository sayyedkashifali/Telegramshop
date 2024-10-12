import asyncio
import logging
import os
import random
import threading
from datetime import datetime

from flask import Flask
from telegram import (ChatMember, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

# Import the admin panel and admin user IDs
from admin.panel import ADMIN_USER_IDS, admin_panel_conv_handler

# Import shop handlers
from free_shop import free_shop_handler  # Make sure this import is correct
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = os.environ.get("BOT_TOKEN")

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Your channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG)  # Set to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

# --- Flask App ---
app = Flask(__name__)


# --- Your Flask routes ---
@app.route('/')
def index():
    return "Hello from Flask!"


# --- Check Membership ---
async def check_membership(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    # ... (your existing check_membership function code) ...


# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing start function code) ...


# --- Button Handlers ---
async def profile_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing profile_handler function code) ...


async def referral_handler(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing referral_handler function code) ...


async def admin_panel_handler(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing admin_panel_handler function code) ...


async def deposit_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing deposit_handler function code) ...


def run_flask_app():
    print("Starting Flask app...")
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)),
            debug=False)  # Disable debug mode for production
    print("Flask app started successfully!")


def run_telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", check_membership))
    application.add_handler(
        CallbackQueryHandler(profile_handler, pattern='profile'))
    application.add_handler(
        CallbackQueryHandler(free_shop_handler,
                             pattern='free_shop'))  # Correct the handler name
    application.add_handler(
        CallbackQueryHandler(paid_shop_handler, pattern='paid_shop'))
    application.add_handler(
        CallbackQueryHandler(referral_handler, pattern='referral'))
    application.add_handler(
        CallbackQueryHandler(admin_panel_handler, pattern='admin'))
    application.add_handler(
        CallbackQueryHandler(deposit_handler, pattern='deposit'))

    # Use asyncio.run() to run the bot in a new event loop
    asyncio.run(application.run_polling())


# --- Main Function ---
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    bot_thread = threading.Thread(target=run_telegram_bot)

    flask_thread.start()
    bot_thread.start()
  
