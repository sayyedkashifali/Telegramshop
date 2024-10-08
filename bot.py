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
    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Initialize Flask app ---
app = Flask(__name__)

# --- Check Membership ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Checks if the user has joined the required channel."""
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL,
                                                   user_id=user.id)

    if chat_member.status in [
            ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR
    ]:
        # User is a member, proceed with the bot's functionality
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


# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    keyboard = [[
        InlineKeyboardButton("Profile", callback_data='profile'),
        InlineKeyboardButton("Free Shop", callback_data='free_shop')
    ], [
        InlineKeyboardButton("Paid Shop", callback_data='paid_shop'),
        InlineKeyboardButton("Referral System", callback_data='referral')
    ],
                [
                    InlineKeyboardButton("Admin Panel", callback_data='admin'),
                    InlineKeyboardButton("Deposit", callback_data='deposit')
                ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message,
                                    reply_markup=reply_markup,
                                    parse_mode="HTML")


# --- Button Handlers ---
async def profile_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Profile' button."""
    user_id = update.effective_user.id
    # You need to implement logic to fetch user details from a database
    username = "test_user"
    transaction_count = 5
    referral_count = 2

    message = f"""
    *User ID:* {user_id}
    *Username:* {username}
    *Transactions:* {transaction_count}
    *Referrals:* {referral_count}
    """
    await update.callback_query.message.edit_text(text=message,
                                                parse_mode='Markdown')


async def referral_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    user_id = update.effective_user.id
    referral_link = f"https://t.me/your_bot?start={user_id}"  # Replace with your actual bot username
    message = f"Share this link to invite others: {referral_link}"
    await update.callback_query.message.edit_text(text=message)


async def admin_panel_handler(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    await admin_panel(update, context)


async def deposit_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    with open('qr_code.png', 'rb') as qr_code_file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=qr_code_file,
            caption=
            "Pay This QR (PayTM) and click Paid button For Go To Next step.\nOr\nYou Can 📞 contact Our Admin And topup Your account."
        )

    # Create the "Paid" and "Admin" buttons
    keyboard = [[
        InlineKeyboardButton("Paid", callback_data='paid'),
        InlineKeyboardButton("Admin", url='https://t.me/your_admin_username')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        "If You paid, Send us a screenshot.\n\nNote :-\nIf You send Fake proofs You will be permanently banned.",
        reply_markup=reply_markup)


# --- Error handler ---
async def error_handler(update: object,
                        context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the developer."""
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)


# --- Flask routes ---
@app.route('/' + TOKEN, methods=['POST'])
async def webhook():
    """Webhook route for Telegram updates."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'OK'

@app.route('/')
def index():
    """Simple index route."""
    return 'Hello, this is the Telegram bot!'


if __name__ == "__main__":
    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()

    # --- Add handlers ---
    application.add_handler(CommandHandler("start", check_membership))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(profile_handler, pattern="profile"))
    application.add_handler(CallbackQueryHandler(free_shop_handler, pattern="free_shop"))  # Connect the handler
    application
  
