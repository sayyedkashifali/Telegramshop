import os
import logging
import random
from datetime import datetime

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ChatMember)
from telegram.ext import (Application, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters, ConversationHandler)

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel_conv_handler, ADMIN_USER_IDS

# Import shop handlers
from free_shop import free_shop_handler
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = "8085073135:AAEpv0Vt56MPYpYAVmyjwmwUvGBcUFIzs6E"  # Your bot token

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Your channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG)  # Set to DEBUG for more detailed logs
logger = logging.getLogger(__name__)


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


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", check_membership))

    # Callback query handlers for buttons
    application.add_handler(
        CallbackQueryHandler(profile_handler, pattern='profile'))
    application.add_handler(
        CallbackQueryHandler(free_shop_handler, pattern='free_shop'))
    application.add_handler(
        CallbackQueryHandler(paid_shop_handler, pattern='paid_shop'))
    application.add_handler(
        CallbackQueryHandler(referral_handler, pattern='referral'))
    application.add_handler(
        CallbackQueryHandler(admin_panel_handler, pattern='admin'))
    application.add_handler(
        CallbackQueryHandler(deposit_handler, pattern='deposit'))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()
  
