import logging
import random
from datetime import datetime
import time
import threading
import os

from flask import Flask
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ChatMember)
from telegram.ext import (Application, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel_conv_handler, ADMIN_USER_IDS
from free_shop import free_shop_handler
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = os.environ.get("BOT_TOKEN")

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"
LOG_CHANNEL_ID = "-1002429063387"

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --- Flask App ---
app = Flask(__name__)

# --- Your Flask routes ---
@app.route('/')
def index():
    return "Hello from Flask!"

# --- Check Membership ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (your existing check_membership function code) ...

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing start function code) ...

# --- Button Handlers ---
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Profile' button."""
    logger.debug("Entering profile_handler")
    try:
        user_id = update.effective_user.id
        # Implement logic to fetch user details from the database
        # For now, using placeholder data
        username = "test_user"
        transaction_count = 5
        referral_count = 2

        message = f"""
        *User ID:* {user_id}
        *Username:* {username}
        *Transactions:* {transaction_count}
        *Referrals:* {referral_count}
        """
        await update.callback_query.message.edit_text(text=message, parse_mode='Markdown')
    except Exception as e:
        logger.exception(f"An error occurred in profile_handler: {e}")

async def referral_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    logger.debug("Entering referral_handler")
    try:
        user_id = update.effective_user.id
        referral_link = f"https://t.me/your_bot?start={user_id}"  # Replace with your actual bot username
        message = f"Share this link to invite others: {referral_link}"
        await update.callback_query.message.edit_text(text=message)
    except Exception as e:
        logger.exception(f"An error occurred in referral_handler: {e}")

async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    logger.debug("Entering admin_panel_handler")
    try:
        await admin_panel_conv_handler(update, context)
    except Exception as e:
        logger.exception(f"An error occurred in admin_panel_handler: {e}")

async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    logger.debug("Entering deposit_handler")
    try:
        with open('qr_code.png', 'rb') as qr_code_file:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=qr_code_file)
    except Exception as e:
        logger.exception(f"An error occurred in deposit_handler: {e}")

def run_flask_app():
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    print("Flask app started successfully!")

def run_telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", check_membership))
    application.add_handler(CallbackQueryHandler(profile_handler, pattern='profile'))
    application.add_handler(CallbackQueryHandler(free_shop_handler, pattern='free_shop'))
    application.add_handler(CallbackQueryHandler(paid_shop_handler, pattern='paid_shop'))
    application.add_handler(CallbackQueryHandler(referral_handler, pattern='referral'))
    application.add_handler(CallbackQueryHandler(admin_panel_handler, pattern='admin'))
    application.add_handler(CallbackQueryHandler(deposit_handler, pattern='deposit'))

    while True:
        try:
            application.run_polling()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            time.sleep(10)

# --- Main Function ---
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    bot_thread = threading.Thread(target=run_telegram_bot)

    flask_thread.start()
    bot_thread.start()
      
