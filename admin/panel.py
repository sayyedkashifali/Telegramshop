from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler

# ... other imports

ADMIN_USER_IDS = [5881638979, 5463285002]  # Updated admin IDs

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the main admin panel menu."""
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        # Get the admin's user ID
        admin_id = update.effective_user.id

        # Send the welcome photo
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://files.catbox.moe/x79o1v.jpg",  # Replace with the actual photo URL
            caption=f"Welcome to the Admin Panel, Admin {admin_id}!"
        )

        # Display admin panel options
        keyboard = [
            [InlineKeyboardButton("Users", callback_data='users')],
            [InlineKeyboardButton("Referrals", callback_data='referrals')],
            [InlineKeyboardButton("Shop", callback_data='shop')],
            [InlineKeyboardButton("Broadcast", callback_data='broadcast')],
            [InlineKeyboardButton("Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Admin Panel:", reply_markup=reply_markup)
        return ADMIN_MENU  # Return the state for the conversation handler
    else:
        await update.message.reply_text("You do not have access to the admin panel.")
        return ConversationHandler.END  # End the conversation if not an admin
