from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database import get_free_products, connect_db  # Import necessary functions

async def free_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Free Shop' button."""
    try:
        client = connect_db()
        db = client["Flexer_Premium_Shop"]
        products = get_free_products(db)
        client.close()  # Close the connection after fetching products

        keyboard = []
        for product in products:
            # Extract relevant product information
            product_id = product.get("product_id")
            name = product.get("name")
            description = product.get("description")
            # ... (add more fields as needed)

            # Create a button for each product with a short description
            button_text = f"{name}\n{description[:50]}..."  # Truncate description if too long
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"product_{product_id}")])

        # Add a "Back" button to return to the main menu
        keyboard.append([InlineKeyboardButton("Back", callback_data="back_to_main")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(
            text="Free Shop:\nChoose a product to view details:",  # Improved message
            reply_markup=reply_markup)

    except Exception as e:
        print(f"Error in free_shop_handler: {e}")
        await update.callback_query.message.edit_text(
            text="An error occurred while fetching products.")
