import os
import logging
import random
import asyncio
from datetime import datetime
from flask import Flask, request, abort
from telegram import (ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update, Poll, PollOption)
from telegram.ext import (Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, PollHandler)

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

# --- Webhook Route for Telegram ---
@app.route('/')
def index():
    """Test route to ensure server is running."""
    return "Hello from Sir! Kashif's Bot is running!"

@app.route('/webhook/<token>', methods=['POST'])
def webhook_handler(token):
    """Handles incoming webhook updates from Telegram."""
    if token != TOKEN:
        logger.warning("Invalid webhook token")
        abort(403)
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
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

# --- Help Command Handler ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    logger.debug("Entering help handler")
    try:
        await update.message.reply_text(
            "Here are the available commands:\n"
            "/start - Start the bot\n"
            "/help - Get help\n"
            "/settings - Manage your settings\n"
            "/quiz - Start a quiz\n"
            "/weather - Get the current weather\n"
        )
    except Exception as e:
        logger.exception(f"Error in help handler: {e}")

# --- Settings Command Handler ---
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /settings command."""
    logger.debug("Entering settings handler")
    try:
        await update.message.reply_text("Settings are currently under development.")
    except Exception as e:
        logger.exception(f"Error in settings handler: {e}")

# --- Quiz Command Handler ---
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /quiz command."""
    logger.debug("Entering quiz handler")
    try:
        question = "What is the capital of France?"
        options = ["Berlin", "Madrid", "Paris", "Rome"]
        await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question,
            options=options,
            is_anonymous=False,
            type=Poll.QUIZ,
            correct_option_id=2
        )
    except Exception as e:
        logger.exception(f"Error in quiz handler: {e}")

# --- Weather Command Handler ---
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /weather command."""
    logger.debug("Entering weather handler")
    try:
        location = "London"
        api_key = "your_openweather_api_key"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        async with context.bot.session.get(weather_url) as response:
            weather_data = await response.json()
            if weather_data["cod"] != 200:
                await update.message.reply_text("Error getting weather data.")
            else:
                weather_desc = weather_data["weather"][0]["description"]
                temp = weather_data["main"]["temp"]
                await update.message.reply_text(f"The weather in {location} is {weather_desc} with a temperature of {temp}K.")
    except Exception as e:
        logger.exception(f"Error in weather handler: {e}")

# --- Poll Answer Handler ---
async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles poll answers."""
    logger.debug("Entering poll answer handler")
    try:
        poll_id = update.poll_answer.poll_id
        selected_option = update.poll_answer.option_ids[0]
        logger.info(f"Poll {poll_id} answered with option {selected_option}.")
    except Exception as e:
        logger.exception(f"Error in poll answer handler: {e}")

# --- Setup Dispatcher ---
def setup_dispatcher():
    """Sets up the Telegram dispatcher with handlers."""
    from telegram import Bot

    bot = Bot(token=TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", check_membership))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(PollHandler(receive_poll_answer))

    # Add callback query handlers
    application.add_handler(CallbackQueryHandler(admin_panel_handler, pattern="^admin$"))
    application.add_handler(CallbackQueryHandler(free_shop_handler, pattern="^free_shop$"))
    application.add_handler(CallbackQueryHandler(paid_shop_handler, pattern="^paid_shop$"))
    application.add_handler(CallbackQueryHandler(referral_system_handler, pattern="^referral$"))
    application.add_handler(CallbackQueryHandler(deposit_handler, pattern="^deposit$"))

    # Add admin conversation handler
    application.add_handler(admin_panel_conv_handler)

    return application

# --- Set Webhook ---
async def set_webhook(application):
    """Sets the Telegram webhook."""
    webhook_url = "https://final-hester-notcrazyhuman-94126448.koyeb.app/"
    if webhook_url:
        success = await application.bot.set_webhook(webhook_url)
        if success:
            logger.info(f"Webhook set to {webhook_url}")
        else:
            logger.error("Failed to set webhook")
    else:
        logger.error("WEBHOOK_URL not set in environment variables.")

# --- Initialize Application ---
if __name__ == "__main__":
    application = setup_dispatcher()
    asyncio.run(set_webhook(application))
    # Run Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
