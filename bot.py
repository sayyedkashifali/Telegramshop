import logging
import random
from datetime import datetime

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ChatMember)
from telegram.ext import (Application, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

from flask import Flask, request

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel, ADMIN_USER_IDS

# Import shop handlers
from free_shop import free_shop_handler
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = "8085073135:AAEpv0Vt56MPYpYAVmyjwmwUvGBcUFIzs6E"  # Your new bot token

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Your channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Set to DEBUG for more detailed logs
)
logger = logging.getLogger(__name__)

# --- Initialize Flask app ---
app = Flask(__name__)

# --- Check Membership ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Checks if the user has joined the required channel."""
    logger.debug("Entering check_membership handler") # Log function entry
    try:
        user = update.effective_user
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL,
                                                       user_id=user.id)

        if chat_member.status in [
                ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR
        ]:
            # User is a member, proceed with the bot's functionality
            logger.debug("User is a member")
            await start(update, context)  # Call the start function here
        else:
            # User is not a member, send a message asking them to join
            join_link = f"https://t.me/{REQUIRED_CHANNEL.removeprefix('@')}"
            keyboard = InlineKeyboardMarkup.from_button(
                InlineKeyboardButton("Join Channel", url=join_link))

            # List of image URLs
            images = [
                "https://files.catbox.moe/z131hg.jpg",
                "https://files.catbox.moe/i0cepb.jpg",
                "https://files.catbox.moe/ahpyvy.jpg",
                "https://files.catbox.moe/jrrfdu.jpg",
                "https://files.catbox.moe/m92opv.jpg",
                "https://files.catbox.moe/dt641v.jpg"
            ]
            # Choose a random image from the list
            random_image = random.choice(images)

            await update.message.reply_photo(
                photo=random_image,
                caption=
                f"👋 Hey {user.mention_html()}!\n\nTo use this bot, you need to join our channel first. Click the button below to join and then press /start to start using the bot.",
                reply_markup=keyboard,
                parse_mode="HTML")
    except Exception as e:
        logger.exception(f"An error occurred in check_membership: {e}") # Log exceptions


# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Entering start handler")
    # ... (rest of your start function)

# ... (rest of your bot.py code with similar logging added to other handlers)

if __name__ == "__main__":
    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()

    # --- Add handlers ---
    # ...

    # --- Set webhook ---
    
