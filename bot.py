import os
import logging
import random
from datetime import datetime
from flask import Flask
from telegram import (ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.ext import (Application, ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters)

# Importing admin and shop handlers
from admin.panel import admin_panel_conv_handler
from free_shop import free_shop_handler
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = os.environ.get("BOT_TOKEN")

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Set to DEBUG for more detailed logs
)
logger = logging.getLogger(__name__)

# --- Flask App ---
app = Flask(__name__)

# --- Flask Routes ---
@app.route('/')
def index():
    return "Hello from Flask!"

# --- Check Membership ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Checks if the user has joined the required channel."""
    logger.debug("Entering check_membership handler")
    try:
        user = update.effective_user
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)

        if chat_member.status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
            logger.debug("User is a member")
            await start(update, context)  # Call start if user is a member
        else:
            join_link = f"https://t.me/{REQUIRED_CHANNEL.removeprefix('@')}"
            keyboard = InlineKeyboardMarkup.from_button(InlineKeyboardButton("Join Channel", url=join_link))

            images = [
                "https://files.catbox.moe/z131hg.jpg", "https://files.catbox.moe/i0cepb.jpg",
                "https://files.catbox.moe/ahpyvy.jpg", "https://files.catbox.moe/jrrfdu.jpg",
                "https://files.catbox.moe/m92opv.jpg", "https://files.catbox.moe/dt641v.jpg"
            ]
            random_image = random.choice(images)

            await update.message.reply_photo(
                photo=random_image,
                caption=f"👋 Hey {user.mention_html()}!\n\nTo use this bot, join our channel first. Click the button below to join and then press /start.",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.exception(f"Error in check_membership: {e}")

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    logger.debug("Entering start handler")
    try:
        user = update.effective_user
        current_hour = datetime.now().hour
        greeting = "Good evening 🌃" if current_hour >= 18 else ("Good afternoon ☀️" if current_hour >= 12 else "Good morning 🌞")

        message = f"""
        {greeting} Hey! {user.mention_html()}

        Welcome to **Flexer Premium Shop** - Your one-stop shop for exclusive deals and premium products. 

        Explore a wide selection of items, manage your orders, and track purchases with ease. We prioritize your satisfaction and a seamless shopping experience.

        Happy shopping! 😊
        """

        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile'), InlineKeyboardButton("Free Shop", callback_data='free_shop')],
            [InlineKeyboardButton("Paid Shop", callback_data='paid_shop'), InlineKeyboardButton("Referral System", callback_data='referral')],
            [InlineKeyboardButton("Admin Panel", callback_data='admin'), InlineKeyboardButton("Deposit", callback_data='deposit')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.exception(f"Error in start handler: {e}")

# --- Admin Panel Handler ---
async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    logger.debug("Entering admin_panel_handler")
    try:
        # Call admin panel conversation handler
        await admin_panel_conv_handler(update, context)
    except Exception as e:
        logger.exception(f"Error in admin_panel_handler: {e}")

# --- Free Shop Handler ---
async def free_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Free Shop' button."""
    logger.debug("Entering free_shop_handler")
    try:
        await free_shop_handler(update, context)  # Call the free shop handler from the import
    except Exception as e:
        logger.exception(f"Error in free_shop_handler: {e}")

# --- Paid Shop Handler ---
async def paid_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Paid Shop' button."""
    logger.debug("Entering paid_shop_handler")
    try:
        await paid_shop_handler(update, context)  # Call the paid shop handler from the import
    except Exception as e:
        logger.exception(f"Error in paid_shop_handler: {e}")

# --- Referral System Handler (Optional) ---
async def referral_system_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    logger.debug("Entering referral_system_handler")
    try:
        await update.message.reply_text("Referral System is currently under development. Stay tuned!")
    except Exception as e:
        logger.exception(f"Error in referral_system_handler: {e}")

# --- Deposit Handler (Optional) ---
async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    logger.debug("Entering deposit_handler")
    try:
        await update.message.reply_text("Deposit functionality is currently under development.")
    except Exception as e:
        logger.exception(f"Error in deposit_handler: {e}")

# --- Initialize the bot application ---
def main():
    try:
        application = ApplicationBuilder().token(TOKEN).build()

        # Command Handlers
        application.add_handler(CommandHandler("start", check_membership))

        # Callback Query Handlers
        application.add_handler(CallbackQueryHandler(start, pattern="^start$"))
        application.add_handler(CallbackQueryHandler(admin_panel_handler, pattern="^admin$"))
        application.add_handler(CallbackQueryHandler(free_shop_handler, pattern="^free_shop$"))
        application.add_handler(CallbackQueryHandler(paid_shop_handler, pattern="^paid_shop$"))
        application.add_handler(CallbackQueryHandler(referral_system_handler, pattern="^referral$"))
        application.add_handler(CallbackQueryHandler(deposit_handler, pattern="^deposit$"))

        # Start the bot
        application.run_polling()
    except Exception as e:
        logger.exception(f"Error in main: {e}")

if __name__ == "__main__":
    main()
