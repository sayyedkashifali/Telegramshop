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

# ... (your users_menu, referrals_menu, shop_menu, broadcast_menu functions)

async def view_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'View Users' button."""
    # ... (fetch and display users from the database)

async def edit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Edit User' button."""
    # ... (get user ID to edit)
    # ... (transition to EDIT_USER_BALANCE state)

async def edit_user_balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle editing the user's balance."""
    try:
        user_id = context.user_data['edit_user_id']  # Get the user ID
        new_balance = float(update.message.text)  # Get the new balance from user input

        # Update the user's balance in the database
        client = database.connect_db()
        db = client[DATABASE_NAME]  # Use the provided database name
        database.update_user_balance(db, user_id, new_balance)
        client.close()

        await update.message.reply_text(f"User {user_id} balance updated to {new_balance}")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid balance. Please enter a valid number.")
        return EDIT_USER_BALANCE
    except Exception as e:
        logger.exception(f"An error occurred while updating user balance: {e}")
        await update.message.reply_text("An error occurred while updating the balance.")
        return ConversationHandler.END

# ... (your back_to_admin_menu, back_to_main_menu functions)

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
