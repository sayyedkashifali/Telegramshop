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
    logger.debug("Entering check_membership handler")
    try:
        user = update.effective_user
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)

        if chat_member.status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
            logger.debug("User is a member")
            await start(update, context)
        else:
            join_link = f"https://t.me/{REQUIRED_CHANNEL.removeprefix('@')}"
            keyboard = InlineKeyboardMarkup.from_button(InlineKeyboardButton("Join Channel", url=join_link))

            images = [
                "https://files.catbox.moe/z131hg.jpg",
                "https://files.catbox.moe/i0cepb.jpg",
            ]
            random_image = random.choice(images)

            await update.message.reply_photo(
                photo=random_image,
                caption=f"👋 Hey {user.mention_html()}!\n\n"
                        f"To use this bot, you need to join our channel first. "
                        f"Click the button below to join and then press /start to start using the bot.",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.exception(f"An error occurred in check_membership: {e}")

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Entering start handler")
    try:
        user = update.effective_user
        current_hour = datetime.now().hour
        greeting = ""

        if 5 <= current_hour < 12:
            greeting = "Good morning 🌞"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon ☀️"
        else:
            greeting = "Good evening 🌃"

        message = f"""
        {greeting} Hey! {user.mention_html()}

        This is **Flexer Premium Shop**, an advanced selling bot designed to provide you with a seamless and secure shopping experience. 

        Explore our wide selection of products, easily manage your orders, and track your purchases with just a few taps. 
        We are committed to providing you with the best possible service and ensuring your satisfaction. 

        Happy shopping! 😊
        """

        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile'),
             InlineKeyboardButton("Free Shop", callback_data='free_shop')],
            [InlineKeyboardButton("Paid Shop", callback_data='paid_shop'),
             InlineKeyboardButton("Referral System", callback_data='referral')],
            [InlineKeyboardButton("Admin Panel", callback_data='admin'),
             InlineKeyboardButton("Deposit", callback_data='deposit')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.exception(f"An error occurred in start: {e}")

# --- Button Handlers ---
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing profile_handler function) ...

async def referral_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing referral_handler function) ...

async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing admin_panel_handler function) ...

async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing deposit_handler function) ...

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
    
