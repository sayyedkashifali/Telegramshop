from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

# ... other imports

ADMIN_USER_IDS = [5881638979, 5463285002]  # Updated admin IDs

# Define states for the conversation
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU = range(5)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # Define admin_panel first
    """Display the main admin panel menu."""
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        # ... (rest of your admin_panel function)

# ... (your users_menu, referrals_menu, shop_menu, broadcast_menu functions)

# ... (your back_to_admin_menu, back_to_main_menu functions)

# ... (your view_users_handler, edit_user_handler functions)

# Create the conversation handler (Now admin_panel is defined before being used)
admin_panel_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        # ... (your states)
    },
    fallbacks=[],
    per_message=True
