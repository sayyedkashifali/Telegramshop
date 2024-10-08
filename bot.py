import logging
import random
from threading import Thread
from flask import Flask, jsonify
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from admin.panel import admin_panel, ADMIN_USER_IDS

# --- Bot Token ---
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"
LOG_CHANNEL_ID = "-1002429063387"

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Flask app for health checks ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify(status="ok")

# --- Check Membership ---
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)
    if chat_member.status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
        await start(update, context)
    else:
        join_link = f"https://t.me/{REQUIRED_CHANNEL.removeprefix('@')}"
        keyboard = InlineKeyboardMarkup.from_button(InlineKeyboardButton("Join Channel", url=join_link))
        images = [
            "https://files.catbox.moe/z131hg.jpg",
            "https://files.catbox.moe/i0cepb.jpg",
            "https://files.catbox.moe/ahpyvy.jpg",
            "https://files.catbox.moe/jrrfdu.jpg",
            "https://files.catbox.moe/m92opv.jpg",
            "https://files.catbox.moe/dt641v.jpg",
            "https://files.catbox.moe/b13ifn.jpg",
            "https://files.catbox.moe/m92opv.jpg",
            "https://files.catbox.moe/jrrfdu.jpg"
        ]
        random_image = random.choice(images)
        await update.message.reply_photo(photo=random_image, caption=f"👋 Hey {user.mention_html()}! To use this bot, you need to join our channel first. Click the button below to join and then press /start to start using the bot.", reply_markup=keyboard, parse_mode="HTML")

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    current_hour = datetime.now().hour
    greeting = "Good evening 🌃" if current_hour >= 18 else "Good afternoon ☀️" if current_hour >= 12 else "Good morning 🌞"
    message = f"""
    {greeting} Hey! {user.mention_html()}
    This is **Flexer Premium Shop**, an advanced selling bot designed to provide you with a seamless and secure shopping experience.
    Explore our wide selection of products, easily manage your orders, and track your purchases with just a few taps.
    We are committed to providing you with the best possible service and ensuring your satisfaction.
    Happy shopping! 😊
    """
    keyboard = [
        [InlineKeyboardButton("Profile", callback_data='profile'), InlineKeyboardButton("Free Shop", callback_data='free_shop')],
        [InlineKeyboardButton("Paid Shop", callback_data='paid_shop'), InlineKeyboardButton("Referral System", callback_data='referral')],
        [InlineKeyboardButton("Admin Panel", callback_data='admin'), InlineKeyboardButton("Deposit", callback_data='deposit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")

# --- Error handler ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

if __name__ == "__main__":
    flask_thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    flask_thread.start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_membership))
    application.run_polling()
