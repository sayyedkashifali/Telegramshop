from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import sqlite3

async def paid_shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the 'Paid Shop' button."""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM products WHERE price > 0")  # Fetch paid products
        products = cursor.fetchall()

        keyboard = []
        for product in products:
            product_id, name, description, price = product  # Adjust columns as needed
            keyboard.append([InlineKeyboardButton(f"{name} - ${price}", callback_data=f"product_{product_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(text="Paid Shop:", reply_markup=reply_markup)

    except Exception as e:
        print(f"Error in paid_shop_handler: {e}")
        await update.callback_query.message.edit_text(text="An error occurred while fetching products.")

    finally:
        conn.close()
      
