from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database import get_paid_products, connect_db  # Import necessary functions

async def paid_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Paid Shop' button."""
    try:
        client = connect_db()
        db = client["Flexer_Premium_Shop"]
        products = get_paid_products(db)
        client.close()

        keyboard = []
        for product in products:
            product_id = product.get("product_id")
            name = product.get("name")
            description = product.get("description")
            price = product.get("price")
            # ... (add more fields as needed)

            button_text = f"{name} - ${price}\n{description[:50]}..."
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"product_{product_id}")])

        keyboard.append([InlineKeyboardButton("Back", callback_data="back_to_main")])  # Back button

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(
            text="Paid Shop:\nChoose a product to view details:",
            reply_markup=reply_markup)

    except Exception as e:
        print(f"Error in paid_shop_handler: {e}")
        await update.callback_query.message.edit_text(
            text="An error occurred while fetching products.")
        
