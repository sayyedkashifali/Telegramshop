import asyncio
import logging
import os
import random
from datetime import datetime
from flask import Flask
from telegram import (ChatMember, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import (Application, ApplicationBuilder,
                          CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)
import threading  # For running Flask and bot concurrently

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
    return "Hello 🇵🇰😝💀🧑‍💻🇵🇰🧑‍💻 From Kashif!"

# --- Check Membership ---
async def check_membership(update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
    """Checks if the user has joined the required channel."""
    logger.debug("Entering check_membership handler")
    try:
        user = update.effective_user
        chat_member = await context.bot.get_chat_member(
            chat_id=REQUIRED_CHANNEL, user_id=user.id)

        if chat_member.status in [
                ChatMember.MEMBER, ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR
        ]:
            # User is a member, proceed with the bot's functionality
            logger.debug("User is a member")
            await start(update, context)
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
        logger.exception(f"An error occurred in check_membership: {e}")

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    logger.debug("Entering start handler")
    try:
        user = update.effective_user
        current_hour = datetime.now().hour
        greeting = ""

        if 5 <= current_hour < 12:
            greeting = "Good morning 🌞"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon ☀️"
        elif 18 <= current_hour < 23:
            greeting = "Good evening 🌃"
        else:
            greeting = "Good night 🌙"

        message = f"""
        {greeting} Hey! {user.mention_html()}

        This is **Flexer Premium Shop**, an advanced selling bot designed to provide you with a seamless and secure shopping experience. 

        Explore our wide selection of products, easily manage your orders, and track your purchases with just a few taps. 
        We are committed to providing you with the best possible service and ensuring your satisfaction. 

        Happy shopping! 😊
        """

        keyboard = [
            [
                InlineKeyboardButton("Profile", callback_data='profile'),
                InlineKeyboardButton("Free Shop", callback_data='free_shop')
            ],
            [
                InlineKeyboardButton("Paid Shop", callback_data='paid_shop'),
                InlineKeyboardButton("Referral System",
                                     callback_data='referral')
            ],
            [
                InlineKeyboardButton("Admin Panel", callback_data='admin'),
                InlineKeyboardButton("Deposit", callback_data='deposit')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message,
                                        reply_markup=reply_markup,
                                        parse_mode="HTML")
    except Exception as e:
        logger.exception(f"An error occurred in start: {e}")

# --- Button Handlers (With Random Images) ---
async def send_random_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random image with a message."""
    logger.debug("Entering send_random_image handler")
    try:
        images = [
            "https://files.catbox.moe/z131hg.jpg",
            "https://files.catbox.moe/i0cepb.jpg",
            "https://files.catbox.moe/ahpyvy.jpg",
            "https://files.catbox.moe/jrrfdu.jpg",
            "https://files.catbox.moe/m92opv.jpg",
            "https://files.catbox.moe/dt641v.jpg"
        ]
        random_image = random.choice(images)

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=random_image,
            caption="Here is a random image for you!"
        )
    except Exception as e:
        logger.exception(f"An error occurred in send_random_image: {e}")

async def profile_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Profile' button."""
    logger.debug("Entering profile_handler")
    try:
        user_id = update.effective_user.id
        # Placeholder data
        username = "test_user"
        transaction_count = 5
        referral_count = 2

        await send_random_image(update, context)  # Send random image

        message = f"""
        *User ID:* {user_id}
        *Username:* {username}
        *Transactions:* {transaction_count}
        *Referrals:* {referral_count}
        """
        await update.callback_query.message.edit_text(text=message,
                                                      parse_mode='Markdown')
    except Exception as e:
        logger.exception(f"An error occurred in profile_handler: {e}")

async def referral_handler(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    logger.debug("Entering referral_handler")
    try:
        user_id = update.effective_user.id
        referral_link = f"https://t.me/your_bot?start={user_id}"  # Replace with your actual bot username

        await send_random_image(update, context)  # Send random image

        message = f"Share this link to invite others: {referral_link}"
        await update.callback_query.message.edit_text(text=message)
    except Exception as e:
        logger.exception(f"An error occurred in referral_handler: {e}")

async def admin_panel_handler(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    logger.debug("Entering admin_panel_handler")
    try:
        await send_random_image(update, context)  # Send random image
        # Assuming your admin panel handler is implemented
    except Exception as e:
        logger.exception(f"An error occurred in admin_panel_handler: {e}")

async def deposit_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    logger.debug("Entering deposit_handler")
    try:
        await send_random_image(update, context)  # Send random image

        # Replace 'qr_code.png' with the actual path to your QR code image
        with open('qr_code.png', 'rb') as qr_code_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code_file,
                caption="Pay This QR (PayTM) and click Paid button to go to the next step.\nOr\nYou can 📞 contact our admin and top up your account."
            )

        # Create the "Paid" and "Admin" buttons
        keyboard = [
            [
                InlineKeyboardButton("Paid", callback_data='paid'),
                InlineKeyboardButton("Admin", url='https://t.me/Sayyed_Kashifali')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text(
            "If you paid, send us a screenshot.\n\nNote:\nIf you send fake proofs, you will be permanently banned.",
            reply_markup=reply_markup)
    except Exception as e:
        logger.exception(f"An error occurred in deposit_handler: {e}")

# --- Run the Flask app on port 8080 ---
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Start the bot ---
async def start_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(profile_handler, pattern='profile'))
