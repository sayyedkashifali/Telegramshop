import logging
import secrets
from threading import Thread

from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackQueryHandler,
                          ChatMemberHandler, ContextTypes, MessageHandler,
                          filters)

# --- Bot Token ---
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"  # Your bot token

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Replace with your channel username
ADMIN_USER_ID = 123456789  # Replace with the actual admin user ID

# --- Enable logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Forced subscription ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check if the user is a member of the required channel."""
    user_id = update.message.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            # User is a member, proceed with bot functionality
            await update.message.reply_text("Welcome! You can now use the bot.")
            await start(update, context)  # Show the main menu
        else:
            # User is not a member, prompt them to join
            await update.message.reply_text(
                f"Please join our channel first: {REQUIRED_CHANNEL}\n"
                "Then, start the bot again."
            )
    except telegram.error.BadRequest as e:
        if str(e) == "User not found":
            # User has not started the channel yet
            await update.message.reply_text(
                f"Please join our channel first: {REQUIRED_CHANNEL}\n"
                "Then, start the bot again."
            )
        else:
            # Handle other potential errors
            logger.error(f"Error checking membership: {e}")

# --- Main menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the main menu with buttons."""
    keyboard = [
        [
            InlineKeyboardButton("Profile", callback_data='profile'),
            InlineKeyboardButton("Free Shop", callback_data='free_shop'),
        ],
        [
            InlineKeyboardButton("Paid Shop", callback_data='paid_shop'),
            InlineKeyboardButton("Referral System", callback_data='referral'),
        ],
        [InlineKeyboardButton("Admin Panel", callback_data='admin')],  # Only for admin
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

# --- Button press handler ---
async def button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        await admin(update, context)  # Call the admin function

# --- Profile function ---
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user's profile information."""
    user_id = update.effective_user.id
    # Fetch user data from database (replace with your database logic)
    user_data = get_user_data(user_id) 
    
    if user_data:
        text = f"Your Profile:\n" \
               f"Transactions: {user_data['transactions']}\n" \
               f"Referral Points: {user_data['referral_points']}\n" \
               f"INR Balance: {user_data['inr_balance']}"
    else:
        text = "You haven't made any transactions yet."
    
    await update.callback_query.message.reply_text(text)

# --- Free shop function ---
async def free_shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the free shop."""
    # Implement free shop logic here
    await update.callback_query.message.reply_text("Welcome to the Free Shop!")

# --- Paid shop function ---
async def paid_shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the paid shop."""
    # Implement paid shop logic here
    await update.callback_query.message.reply_text("Welcome to the Paid Shop!")

# --- Referral system ---
def generate_referral_link(user_id):
    """Generate and store a unique referral link for the user."""
    # Generate a unique referral code (e.g., using secrets.token_urlsafe())
    referral_code = secrets.token_urlsafe(16)
    # Store the referral code in the database, linked to the user_id
    store_referral_code(user_id, referral_code)
    return f"https://t.me/your_bot?start={referral_code}"

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user's referral link."""
    user_id = update.effective_user.id
    referral_link = generate_referral_link(user_id)
    await update.callback_query.message.reply_text(f"Your referral link: {referral_link}")

# --- Admin panel ---
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the admin panel (only for the admin user)."""
    user_id = update.effective_user.id
    if user_id == ADMIN_USER_ID:  # Replace with the actual admin user ID
        # Display admin panel options (e.g., list users, set points, broadcast)
        await update.callback_query.message.reply_text("Welcome to the admin panel!")
    else:
        await update.callback_query.message.reply_text("You do not have access to the admin panel.")

# --- Placeholder functions for database interaction ---
def get_user_data(user_id):
    """Fetch user data from the database (placeholder)."""
    # Replace with your database logic to fetch user data
    # This is a placeholder, return a dictionary with user data
    return {
        'transactions': 5,
        'referral_points': 100,
        'inr_balance': 50.0
    }

def store_referral_code(user_id, referral_code):
    """Store the referral code in the database (placeholder)."""
    # Replace with your database logic to store the referral code
    pass

# --- Flask app for health checks ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Telegram Bot!"

def run_flask_app():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, check_membership))
    application.add_handler(CallbackQueryHandler(button_press))
    # ... (add other handlers)
    application.run_polling()
    
