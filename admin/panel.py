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
    await update.message.reply_text("Users menu selected.")
    return USERS_MENU

# Define the referrals_menu function
async def referrals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Referrals' button in the admin panel."""
    await update.message.reply_text("Referrals menu selected.")
    return REFERRALS_MENU

# Define the shop_menu function
async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Shop' button in the admin panel."""
    await update.message.reply_text("Shop menu selected.")
    return SHOP_MENU

# Define the broadcast_menu function
async def broadcast_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the 'Broadcast' button in the admin panel."""
    await update.message.reply_text("Broadcast menu selected.")
    return BROADCAST_MENU

# Define the edit_user_balance function
async def edit_user_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle editing user balance."""
    await update.message.reply_text("Edit user balance selected.")
    return EDIT_USER_BALANCE

# Additional Feature: View Users
async def view_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle viewing users."""
    await update.message.reply_text("View users selected.")
    return USERS_MENU

# Additional Feature: Edit User
async def edit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle editing a user."""
    await update.message.reply_text("Edit user selected.")
    return USERS_MENU

# Additional Feature: Back to Admin Menu
async def back_to_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle going back to the admin menu."""
    await update.message.reply_text("Returning to admin menu.")
    return ADMIN_MENU

# Additional Feature: Back to Main Menu
async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle going back to the main menu."""
    await update.message.reply_text("Returning to main menu.")
    return ConversationHandler.END

# Define the new user registration function
async def register_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a new user."""
    # Registration logic here
    await update.message.reply_text("New user registered.")
    return USERS_MENU

# Define the user removal function
async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Remove an existing user."""
    # Removal logic here
    await update.message.reply_text("User removed.")
    return USERS_MENU

# Define the referral statistics function
async def referral_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show referral statistics."""
    # Referral stats logic here
    await update.message.reply_text("Referral statistics displayed.")
    return REFERRALS_MENU

# Define the product listing function
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """List all products in the shop."""
    # Product listing logic here
    await update.message.reply_text("Product listing displayed.")
    return SHOP_MENU

# Define the add product function
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Add a new product to the shop."""
    # Add product logic here
    await update.message.reply_text("New product added.")
    return SHOP_MENU

# Define the remove product function
async def remove_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Remove a product from the shop."""
    # Remove product logic here
    await update.message.reply_text("Product removed.")
    return SHOP_MENU

# Define the broadcast message function
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Broadcast a message to all users."""
    # Broadcast message logic here
    await update.message.reply_text("Message broadcasted.")
    return BROADCAST_MENU

# Define the return to previous menu function
async def return_to_previous_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to the previous menu."""
    await update.message.reply_text("Returning to the previous menu.")
    return ADMIN_MENU

# Create the conversation handler
admin_panel_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(admin_panel, pattern="admin")],
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
            CallbackQueryHandler(edit_user_balance, pattern="edit_user_balance")
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
