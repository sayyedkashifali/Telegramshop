from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

from admin.users import set_balance, list_users  # Import admin functions
from admin.utils import broadcast

# --- Admin Panel States ---
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU = range(4)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the main admin panel menu."""
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        keyboard = [
            [InlineKeyboardButton("Users", callback_data='users')],
            [InlineKeyboardButton("Referrals", callback_data='referrals')],
            [InlineKeyboardButton("Shop", callback_data='shop')],
            [InlineKeyboardButton("Broadcast", callback_data='broadcast')],
            [InlineKeyboardButton("Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Admin Panel:", reply_markup=reply_markup)
        return ADMIN_MENU
    else:
        await update.message.reply_text("You do not have access to the admin panel.")
        return ConversationHandler.END

async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button presses in the main admin menu."""
    query = update.callback_query
    await query.answer()

    if query.data == 'users':
        # Display users menu
        keyboard = [
            [InlineKeyboardButton("List Users", callback_data='list_users')],
            [InlineKeyboardButton("Set Balance", callback_data='set_balance')],
            [InlineKeyboardButton("Back", callback_data='back_to_admin')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Users Menu:", reply_markup=reply_markup)
        return USERS_MENU
    elif query.data == 'referrals':
        # Display referrals menu
        await query.edit_message_text("Referrals Menu (Coming Soon)")
        return REFERRALS_MENU
    elif query.data == 'shop':
        # Display shop menu
        await query.edit_message_text("Shop Menu (Coming Soon)")
        return SHOP_MENU
    elif query.data == 'broadcast':
        await broadcast(update, context)
        return ADMIN_MENU
    elif query.data == 'back':
        await query.edit_message_text("Exiting admin panel.")
        return ConversationHandler.END

async def users_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button presses in the users menu."""
    query = update.callback_query
    await query.answer()

    if query.data == 'list_users':
        await list_users(update, context)
        return USERS_MENU
    elif query.data == 'set_balance':
        await query.edit_message_text("Enter user ID and new balance (e.g., `/set_balance 123456789 100`)")
        return USERS_MENU
    elif query.data == 'back_to_admin':
        return await admin_panel(update, context)  # Go back to main admin menu

# --- Admin Panel Conversation Handler ---
admin_panel_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        ADMIN_MENU: [CallbackQueryHandler(admin_menu_handler)],
        USERS_MENU: [
            CallbackQueryHandler(users_menu_handler),
            CommandHandler("set_balance", set_balance)
        ],
        REFERRALS_MENU: [CallbackQueryHandler(admin_menu_handler)],  # Placeholder
        SHOP_MENU: [CallbackQueryHandler(admin_menu_handler)]  # Placeholder
    },
    fallbacks=[CommandHandler("admin", admin_panel)]
        )
