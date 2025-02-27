from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

from admin.users import set_balance, list_users  # Import admin functions
from admin.utils import broadcast

# Updated admin IDs and states
ADMIN_USER_IDS = [5881638979, 5463285002]
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU = range(5)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the main admin panel menu."""
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        admin_id = update.effective_user.id
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://files.catbox.moe/x79o1v.jpg",  # Replace with the actual photo URL
            caption=f"Welcome to the Admin Panel, Admin {admin_id}!"
        )
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

async def users_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the users menu."""
    keyboard = [
        [InlineKeyboardButton("View Users", callback_data='view_users')],
        [InlineKeyboardButton("Edit User", callback_data='edit_user')],
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Users Menu:", reply_markup=reply_markup)
    return USERS_MENU

async def referrals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the referrals menu."""
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Referrals Menu:", reply_markup=reply_markup)
    return REFERRALS_MENU

async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the shop menu."""
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Shop Menu:", reply_markup=reply_markup)
    return SHOP_MENU

async def broadcast_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the broadcast menu."""
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Broadcast Menu:", reply_markup=reply_markup)
    return BROADCAST_MENU

async def back_to_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Back' button to return to the main admin menu."""
    return await admin_panel(update, context)

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Back' button to return to the main menu."""
    from bot import start  # Import start function from bot.py
    await start(update, context)  # Call the start function to display the main menu
    return ConversationHandler.END

async def view_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'View Users' button."""
    # Add your implementation here
    pass

async def edit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Edit User' button."""
    # Add your implementation here
    pass

# Create the conversation handler
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
        REFERRALS_MENU: [
            # ... (Add handlers for referrals menu options)
        ],
        SHOP_MENU: [
            # ... (Add handlers for shop menu options)
        ],
        BROADCAST_MENU: [
            # ... (Add handlers for broadcast menu options)
        ]
    },
    fallbacks=[]  # You might want to add a fallback handler here
)
