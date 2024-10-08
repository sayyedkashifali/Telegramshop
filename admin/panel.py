from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

# ... other imports

ADMIN_USER_IDS = [5881638979, 5463285002]  # Updated admin IDs

# Define states for the conversation
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU = range(5)

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

# ... (your users_menu, referrals_menu, shop_menu, broadcast_menu functions)

# ... (your back_to_admin_menu, back_to_main_menu functions)

# ... (your view_users_handler, edit_user_handler, ourna_function functions)

# Create the conversation handler (Now admin_panel is defined before being used)
admin_panel_conv_handler = ConversationHandler(  # Indented correctly
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
