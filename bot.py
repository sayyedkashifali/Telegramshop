import logging
import random
from datetime import datetime

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ChatMember)
from telegram.ext import (Application, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

# Import the admin panel and admin user IDs from the correct module
from admin.panel import admin_panel, ADMIN_USER_IDS

# --- Bot Token ---
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"  # Replace with your actual bot token

# --- Other settings ---
REQUIRED_CHANNEL = "@igdealsbykashif"  # Your channel username
LOG_CHANNEL_ID = "-1002429063387"  # Your log channel ID

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)


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
            "https://files.catbox.moe/dt641v.jpg",
            "https://files.catbox.moe/b13ifn.jpg",
            "https://files.catbox.moe/m92opv.jpg",
            "https://files.catbox.moe/jrrfdu.jpg"
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
    # ... your database interaction logic to fetch username, transaction_count, referral_count ...

    message = f"""
    *User ID:* {user_id}
    *Username:* {username}
    *Transactions:* {transaction_count}
    *Referrals:* {referral_count}
    """
    await update.callback_query.message.edit_text(text=message,
                                                parse_mode='Markdown')


async def free_shop_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Free Shop' button."""
    # Fetch and display items from the free shop
    # ... your shop logic ...
    pass  # Replace with your actual free shop code


async def paid_shop_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Paid Shop' button."""
    # Fetch and display items from the paid shop
    # ... your shop logic ...
    pass  # Replace with your actual paid shop code


async def referral_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Referral System' button."""
    user_id = update.effective_user.id
    # Generate or fetch the user's unique referral ID
    # ... your referral logic ...
    referral_link = f"https://t.me/your_bot?start={user_id}"  # Replace with your actual bot username
    message = f"Share this link to invite others: {referral_link}"
    await update.callback_query.message.edit_text(text=message)


async def admin_panel_handler(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Admin Panel' button."""
    # Redirect to the admin panel function
    await admin_panel(update, context)


async def deposit_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Deposit' button."""
    # Send the QR code image and instructions
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('qr_code.png', 'rb'),  # Replace with the actual path to your QR code image
        caption=
        "Pay This QR (PayTM) and click Paid button For Go To Next step.\nOr\nYou Can 📞 contact Our Admin And topup Your account."
    )
    # Create the "Paid" and "Admin" buttons
    keyboard = [[
        InlineKeyboardButton("Paid", callback_data='paid'),
        InlineKeyboardButton("Admin",
                             url='https://t.me/your_admin_username')
    ]]  # Replace with your admin's Telegram username
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        "Hey UNKNOWN.\nIf You paid Send us a screenshot.\n\nNote :-\nIf You send Fake proofs You got Permanently banned.",
        reply_markup=reply_markup)


# --- Error handler ---
async def error_handler(update: object,
                        context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the developer."""
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)


if __name__ == "__main__":
    # --- Telegram bot ---
    application = Application.builder().token(TOKEN).build()

    # --- Add handlers ---
    application.add_handler(MessageHandler(filters
    
