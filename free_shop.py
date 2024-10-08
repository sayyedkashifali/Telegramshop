from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import sqlite3

async def free_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Free Shop' button."""
    conn = sqlite3.connect('your_database.db')  # Connect to your database
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM products WHERE price = 0")  # Fetch free products
        products = cursor.fetchall()

        keyboard = []
        for product in products:
            product_id, name, description = product  # Adjust columns as needed
            keyboard.append([InlineKeyboardButton(name, callback_data=f"product_{product_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(text="Free Shop:", reply_markup=reply_markup)

    except Exception as e:
        print(f"Error in free_shop_handler: {e}")  # Basic error handling
        await update.callback_query.message.edit_text(text="An error occurred while fetching products.")

    finally:
        conn.close()
