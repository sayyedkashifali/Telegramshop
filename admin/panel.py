from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

# ... other imports

ADMIN_USER_IDS = [5881638979, 5463285002]  # Updated admin IDs

# Define states for the conversation
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU, EDIT_USER_BALANCE = range(6)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the main admin panel menu."""
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        # ... (rest of your admin_panel function)

async def users_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # Define users_menu before use
    """Display the users menu."""
    # ... (rest of your users_menu function)

# ... (your referrals_menu, shop_menu, broadcast_menu functions)

# ... (your back_to_admin_menu, back_to_main_menu functions)

# ... (your view_users_handler, edit_user_handler, edit_user_balance_handler functions)

# Create the conversation handler (Now users_menu is defined before being used)
admin_panel_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        ADMIN_MENU: [
            CallbackQueryHandler(users_menu, pattern="users"),
            CallbackQueryHandler(referrals_menu, pattern="referrals"),
            CallbackQueryHandler(shop_menu, pattern="shop"),
            CallbackQueryHandler(broadcast_menu, pattern="broadcast"),
            CallbackQueryHandler(back_to_main_menu, pattern="back")
        ],
        USERS_MENU: [
            CallbackQueryHandler(view_users_handler, pattern="view_users"),
            CallbackQueryHandler(edit_user_handler, pattern="edit_user"),
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin")
        ],
        EDIT_USER_BALANCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_user_balance_handler)
        ],
        REFERRALS_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin")
        ],
        SHOP_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin")
        ],
        BROADCAST_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin")
        ]
    },
    fallbacks=[],
    per_message=True
)
