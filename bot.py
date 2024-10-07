import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ChatMemberHandler

# Your bot's API token
TOKEN = "7734029404:AAGjciB3zvBfxMP8XpePT3-mRQLsPAkCY74"  # Replace with your actual bot token

REQUIRED_CHANNEL = "@igdealsbykashif"  # Replace with your channel username

# --- Forced subscription ---
def check_membership(update, context):
    user_id = update.message.from_user.id
    try:
        chat_member = context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            # User is a member, proceed with bot functionality
            context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! You can now use the bot.")
            # ... (show main menu)
        else:
            # User is not a member, prompt them to join
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Please join our channel first: {REQUIRED_CHANNEL}\n"
                                          "Then, start the bot again.")
    except telegram.error.BadRequest as e:
        if str(e) == "User not found":
            # User has not started the channel yet
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Please join our channel first: {REQUIRED_CHANNEL}\n"
                                          "Then, start the bot again.")
        else:
            # Handle other potential errors
            print(f"Error checking membership: {e}")

# --- Main menu ---
def start(update, context):
    # ... (Code for the main menu with buttons)
    pass  # Replace with your main menu implementation

# --- Other functions ---
# ... (Code for profile, free shop, paid shop, referral system, admin panel)

# --- Handlers ---
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Updated filter usage
dispatcher.add_handler(MessageHandler(filters.ALL, check_membership))  
dispatcher.add_handler(CommandHandler("start", start))
# ... (add other handlers)

updater.start_polling()
updater.idle()
