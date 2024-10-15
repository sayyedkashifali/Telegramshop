import os
import logging
import random
from datetime import datetime
from flask import Flask, request, jsonify, abort
from telegram import (ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.ext import (Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes)

# Importing admin and shop handlers
from admin.panel import admin_panel_conv_handler
from free_shop import free_shop_handler
from paid_shop import paid_shop_handler

# --- Bot Token ---
TOKEN = os.environ.get("BOT_TOKEN")

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"
LOG_CHANNEL_ID = "-1002429063387"

# --- Flask App ---
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # DEBUG level for detailed logs
)
logger = logging.getLogger(__name__)

# Initialize application
application = ApplicationBuilder().token(TOKEN).build()

# --- Test Route ---
@app.route('/')
def index():
    """Test route to ensure server is running."""
    return "Hello from Sir! Kashif's Bot is running!"

# --- Webhook Route ---
@app.route('/webhook/<token>', methods=['POST'])
def webhook_handler(token):
    """Handles incoming webhook updates from Telegram."""
    if token != TOKEN:
        logger.warning("Invalid webhook token")
        abort(403)

    try:
        update = Update.de_json(request.get_json(force=True), bot=application.bot)
        application.update_queue.put(update)
        return "OK", 200
    except Exception as e:
        logger.exception(f"Error processing webhook: {e}")
        return "Internal Server Error", 500

# --- Check Membership Function ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the user is a member of the required channel."""
    logger.debug("Entering check_membership handler")
    try:
        user = update.effective_user
        chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)

        if chat_member.status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
            logger.debug("User is a member")
            await start(update, context)
        else:
            join_link = f"https://t.me/{REQUIRED_CHANNEL.removeprefix('@')}"
            keyboard = InlineKeyboardMarkup.from_button(
                InlineKeyboardButton("Join Channel", url=join_link)
            )

            images = [
                "https://files.catbox.moe/z131hg.jpg",
                "https://files.catbox.moe/i0cepb.jpg",
                "https://files.catbox.moe/ahpyvy.jpg",
                "https://files.catbox.moe/jrrfdu.jpg",
                "https://files.catbox.moe/m92opv.jpg",
                "https://files.catbox.moe/dt641v.jpg"
            ]
            random_image = random.choice(images)

            await update.message.reply_photo(
                photo=random_image,
                caption=(
                    f"👋 Hey {user.mention_html()}!\n\nTo use this bot, you need to join our channel first. "
                    "Click the button below to join and then press /start to begin using the bot."
                ),
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.exception(f"Error in check_membership: {e}")

# --- Start Command Handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    logger.debug("Entering start handler")
    try:
        user = update.effective_user
        current_hour = datetime.now().hour
        greeting = (
            "Good evening 🌃" if current_hour >= 18 else 
            ("Good afternoon ☀️" if current_hour >= 12 else "Good morning 🌞")
        )

        message = f"""
        {greeting} Hey! {user.mention_html()}

        Welcome to **Flexer Premium Shop** - Your one-stop shop for exclusive deals and premium products.

        Explore a wide selection of items, manage your orders, and track purchases with ease. We prioritize your satisfaction and a seamless shopping experience.

        Happy shopping! 😊
        """

        keyboard = [
            [
                InlineKeyboardButton("Profile", callback_data='profile'),
                InlineKeyboardButton("Free Shop", callback_data='free_shop')
            ],
            [
                InlineKeyboardButton("Paid Shop", callback_data='paid_shop'),
                InlineKeyboardButton("Referral System", callback_data='referral')
            ],
            [
                InlineKeyboardButton("Admin Panel", callback_data='admin'),
                InlineKeyboardButton("Deposit", callback_data='deposit')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.exception(f"Error in start handler: {e}")

# --- Referral System Handler ---
async def referral_system_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    logger.debug("Entering referral_system_handler")
    try:
        await update.callback_query.message.edit_text("Referral System is currently under development.")
    except Exception as e:
        logger.exception(f"Error in referral_system_handler: {e}")

# --- Deposit Handler ---
async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    logger.debug("Entering deposit_handler")
    try:
        with open('qr_code.png', 'rb') as qr_code_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code_file,
                caption="Pay this QR (PayTM) and click Paid to proceed.\nOr contact our admin for top-up."
            )

        keyboard = [
            [
                InlineKeyboardButton("Paid", callback_data='paid'),
                InlineKeyboardButton("Admin", url='https://t.me/Sayyed_Kashifali')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(
            "If you have paid, send us a screenshot.\n\nNote:\nSending fake proofs will result in a permanent ban.",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.exception(f"Error in deposit_handler: {e}")

# --- Free Shop Handler ---
async def free_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Free Shop' button."""
    logger.debug("Entering free_shop_handler")
    try:
        await update.callback_query.message.edit_text("Welcome to the Free Shop!")
    except Exception as e:
        logger.exception(f"Error in free_shop_handler: {e}")

# --- Paid Shop Handler ---
async def paid_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Paid Shop' button."""
    logger.debug("Entering paid_shop_handler")
    try:
        await update.callback_query.message.edit_text("Welcome to the Paid Shop!")
    except Exception as e:
        logger.exception(f"Error in paid_shop_handler: {e}")

# --- Admin Panel Handler ---
async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    logger.debug("Entering admin_panel_handler")
    try:
        await admin_panel_conv_handler.process_update(update, context)
    except Exception as e:
        logger.exception(f"Error in admin_panel_handler: {e}")

# --- Setup Dispatcher ---
def setup_dispatcher():
    """Sets up the Telegram dispatcher with handlers."""
    # Add handlers
    application.add_handler(CommandHandler("start", check_membership))
    application.add_handler(CallbackQueryHandler(admin_panel_handler, pattern="^admin$"))
    application.add_handler(CallbackQueryHandler(free_shop_handler, pattern="^free_shop$"))
    application.add_handler(CallbackQueryHandler(paid_shop_handler, pattern="^paid_shop$"))
    application.add_handler(CallbackQueryHandler(referral_system_handler, pattern="^referral$"))
    application.add_handler(CallbackQueryHandler(deposit_handler, pattern="^deposit$"))

    # Add admin conversation handler
    application.add_handler(admin_panel_conv_handler)

# --- Set Webhook ---
def set_webhook():
    """Sets the Telegram webhook."""
    webhook_url = os.environ.get("https://eoc94fq6ah6cxu4.m.pipedream.net")   # e.g., https://your-koyeb-app.koyeb.app/webhook/<token>
    if webhook_url:
        success = application.bot.set_webhook(webhook_url)
        if success:
            logger.info(f"Webhook set to {webhook_url}")
        else:
            logger.error("Failed to set webhook")
    else:
        logger.error("WEBHOOK_URL not set in environment variables.")

# --- Initialize App ---
if __name__ == "__main__":
    setup_dispatcher()
    set_webhook()
    # Run Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
