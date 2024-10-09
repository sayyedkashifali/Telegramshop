from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler

import database  # Import the database module

# Get the database name from database.py
DATABASE_NAME = "Flexer_Premium_Shop"  # Use the provided database name

# Admin user IDs (replace with actual IDs)
ADMIN_USER_IDS = [5881638979, 5463285002]

# Define states for the conversation
ADMIN_MENU, USERS_MENU, REFERRALS_MENU, SHOP_MENU, BROADCAST_MENU, EDIT_USER_BALANCE = range(6)

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
        return ADMIN_MENU
    else:
        await update.message.reply_text("You do not have access to the admin panel.")
        return ConversationHandler.END

# Define the users_menu function
async def users_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Users' button in the admin panel."""
    # Your logic to handle users menu goes here
    await update.message.reply_text("Users menu selected.")
    return USERS_MENU

# Define other necessary functions (referrals_menu, shop_menu, broadcast_menu, etc.)

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
