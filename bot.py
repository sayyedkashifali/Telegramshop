import logging
from threading import Thread
from telegram.ext import CallbackQueryHandler
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel, ADMIN_USER_IDS

# --- Bot Token ---
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Your channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Log user information ---
async def log_user_info(update: Update,
                        context: ContextTypes.DEFAULT_TYPE,
                        user_id,
                        message):
    """Log user information to the log channel."""
    try:
        await context.bot.send_message(chat_id=LOG_CHANNEL_ID,
                                       text=f"User ID: {user_id}\n{message}")
    except Exception as e:
        logger.error(f"Error logging user info: {e}")

# --- Forced subscription ---
async def check_membership(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ensure the user is a member of the required channel."""
    if update.effective_user is None:
        logger.error("No effective user found in the update.")
        return

    user_id = update.effective_user.id
    try:
        member_status = await context.bot.get_chat_member(REQUIRED_CHANNEL,
                                                            user_id)
        if member_status.status == "left":
            await update.message.reply_text(
                f"You must join {REQUIRED_CHANNEL} to use this bot.")
            return
        else:
            await start(update, context)
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        
# --- Main menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the main menu."""
    # Simpler menu for debugging
    keyboard = [
        [InlineKeyboardButton("Send Test Message", callback_data="send_message")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Bot!",
                                    reply_markup=reply_markup)

# --- Button press handler ---
async def button_press(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses from the main menu."""
    query = update.callback_query
    await query.answer()

    if query.data == "send_message":
        await send_test_message(update, context)

async def send_test_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a test message to the user."""
    try:
        await update.callback_query.message.reply_text("This is a test message!")
    except Exception as e:
        logger.error(f"Error sending test message: {e}")

# --- Placeholder functions for database interaction ---
def get_user_data(user_id):
    """Fetch user data from the database (placeholder)."""
    return {
        "transactions": 5,
        "referral_points": 100,
        "inr_balance": 0.0  # New users start with 0 INR balance
    }

# --- Flask app for health checks ---
# ... (Flask app code remains the same)

if __name__ == "__main__":
    # ... (Flask thread remains the same)

    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()

    # --- Add handlers ---
    application.add_handler(MessageHandler(filters.ALL, check_membership))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("admin", admin_panel))

    # Add other handlers if needed
    application.add_handler(CommandHandler("start", start))

    application.run_polling()
  
