from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

ADMIN_USER_IDS = [5881638979, 5463285002]

ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU = range(5)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id in ADMIN_USER_IDS:
        admin_id = update.effective_user.id

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://files.catbox.moe/x79o1v.jpg",
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
    keyboard = [
        [InlineKeyboardButton("View Users", callback_data='view_users')],
        [InlineKeyboardButton("Edit User", callback_data='edit_user')],
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Users Menu:", reply_markup=reply_markup)
    return USERS_MENU

async def referrals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Referrals Menu:", reply_markup=reply_markup)
    return REFERRALS_MENU

async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Shop Menu:", reply_markup=reply_markup)
    return SHOP_MENU

async def broadcast_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Back", callback_data='back_to_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Broadcast Menu:", reply_markup=reply_markup)
    return BROADCAST_MENU

async def back_to_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await admin_panel(update, context)

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    from bot import start
    await start(update, context)
    return ConversationHandler.END

async def view_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def edit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

# Updated conversation handler with fallbacks
# Example of updating CallbackQueryHandler with per_message=True
admin_panel_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        ADMIN_MENU: [
            CallbackQueryHandler(users_menu, pattern="users", per_message=True),
            CallbackQueryHandler(referrals_menu, pattern="referrals", per_message=True),
            CallbackQueryHandler(shop_menu, pattern="shop", per_message=True),
            CallbackQueryHandler(broadcast_menu, pattern="broadcast", per_message=True),
            CallbackQueryHandler(back_to_main_menu, pattern="back", per_message=True)
        ],
        USERS_MENU: [
            CallbackQueryHandler(view_users_handler, pattern="view_users", per_message=True),
            CallbackQueryHandler(edit_user_handler, pattern="edit_user", per_message=True),
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin", per_message=True)
        ],
        REFERRALS_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin", per_message=True)
        ],
        SHOP_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin", per_message=True)
        ],
        BROADCAST_MENU: [
            CallbackQueryHandler(back_to_admin_menu, pattern="back_to_admin", per_message=True)
        ]
    },
    fallbacks=[CommandHandler("cancel", back_to_main_menu)]  # Added fallback
)
