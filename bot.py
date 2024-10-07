import logging
import secrets
from threading import Thread

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler,
                          ChatMemberHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel, ADMIN_USER_IDS

# --- Bot Token ---
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"  # Replace with your actual bot token

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Replace with your actual channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Log user information ---
async def log_user_info(update: Update,
                        context: ContextTypes.DEFAULT_TYPE,
                        user_id,
                        message):
    """Log user information to the log channel."""
    try:
        await context.bot.send_message(
            chat_id=LOG_CHANNEL_ID,
            text=f"User ID: {user_id}\n{message}")
    except Exception as e:
        logger.error(f"Error logging user info: {e}")

# --- Forced subscription ---
async def check_membership(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ensure the user is a member of the required channel."""
    user_id = update.effective_user.id
    try:
        member_status = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member_status.status == 'left':
            await update.message.reply_text(
                f"You must join {REQUIRED_CHANNEL} to use this bot."
            )
            return
    except Exception as e:
        logger.error(f"Error checking membership: {e}")

# --- Main menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the main menu."""
    keyboard = [
        [InlineKeyboardButton("Profile", callback_data='profile')],
        [InlineKeyboardButton("Free Shop", callback_data='free_shop')],
        [InlineKeyboardButton("Paid Shop", callback_data='paid_shop')],
        [InlineKeyboardButton("Referral", callback_data='referral')],
        [InlineKeyboardButton("Admin", callback_data='admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Bot!", reply_markup=reply_markup)

# --- Button press handler ---
async def button_press(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses from the main menu."""
    query = update.callback_query
    await query.answer()

    if query.data == 'profile':
        await profile(update, context)  # Call the profile function
    elif query.data == 'free_shop':
        await free_shop(update, context)  # Call the free_shop function
    elif query.data == 'paid_shop':
        await paid_shop(update, context)  # Call the paid_shop function
    elif query.data == 'referral':
        await referral(update, context)  # Call the referral function
    elif query.data == 'admin':
        await admin_panel(update, context)  # Call the admin function

# --- Profile function ---
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user's profile information."""
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    profile_info = (f"Transactions: {user_data['transactions']}\n"
                    f"Referral Points: {user_data['referral_points']}\n"
                    f"INR Balance: {user_data['inr_balance']}")
    await update.callback_query.message.reply_text(profile_info)

# --- Free shop function ---
async def free_shop(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the free shop."""
    # Implement free shop logic here
    await update.callback_query.message.reply_text("Welcome to the Free Shop!")

# --- Paid shop function ---
async def paid_shop(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the paid shop."""
    # Implement paid shop logic here
    await update.callback_query.message.reply_text("Welcome to the Paid Shop!")

# --- Referral system ---
def generate_referral_link(user_id):
    """Generate and store a unique referral link for the user."""
    referral_code = secrets.token_urlsafe(16)
    # store_referral_code(user_id, referral_code)  # Implement in database.py
    return f"https://t.me/Teshfjsgfsudb_bot?start={referral_code}"

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user's referral link."""
    user_id = update.effective_user.id
    referral_link = generate_referral_link(user_id)
    await update.callback_query.message.reply_text(
        f"Your referral link: {referral_link}")

# --- Placeholder functions for database interaction ---
def get_user_data(user_id):
    """Fetch user data from the database (placeholder)."""
    # Replace with your database logic to fetch user data
    # This is a placeholder, return a dictionary with user data
    return {
        'transactions': 5,
        'referral_points': 100,
        'inr_balance': 0.0  # New users start with 0 INR balance
    }

# --- Flask app for health checks ---
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify(status='ok')

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = Thread(target=app.run, kwargs={'port': 5000})
    flask_thread.start()

    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, check_membership))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("admin", admin_panel))
    # Add other handlers if needed
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
