# database.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# MongoDB connection string
MONGO_URI = "mongodb+srv://arevaloju136:D8d1QVGTmM6PqM9A@cluster0.c2brp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_db():
    """Connects to the MongoDB database."""
    try:
        client = MongoClient(MONGO_URI)
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except ConnectionFailure:
        print("Failed to connect to MongoDB.")
        return None

def create_collections(db):
    """Creates the necessary collections if they don't exist."""
    collections = [
        {"name": "products", "fields": ["product_id", "name", "description", "price", "image_url"]},
        {"name": "users", "fields": ["user_id", "username", "balance", "referral_count"]},
        {"name": "orders", "fields": ["order_id", "user_id", "product_id", "quantity", "timestamp"]}
    ]

    for collection_data in collections:
        collection_name = collection_data["name"]
        if collection_name not in db.list_collection_names():
            print(f"Creating collection: {collection_name}")
            db.create_collection(collection_name)

def add_product(db, name, description, price, image_url):
    """Adds a new product to the database."""
    try:
        products_collection = db["products"]
        product_id = products_collection.count_documents({}) + 1  # Simple auto-increment
        product = {
            "product_id": product_id,
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url
        }
        result = products_collection.insert_one(product)
        print(f"Added product with ID: {result.inserted_id}")
    except OperationFailure as e:
        print(f"Error adding product: {e}")

def get_product(db, product_id):
    """Retrieves a product from the database."""
    try:
        products_collection = db["products"]
        product = products_collection.find_one({"product_id": product_id})
        return product
    except OperationFailure as e:
        print(f"Error getting product: {e}")
        return None

def update_product(db, product_id, name, description, price, image_url):
    """Updates a product in the database."""
    try:
        products_collection = db["products"]
        result = products_collection.update_one(
            {"product_id": product_id},
            {"$set": {"name": name, "description": description, "price": price, "image_url": image_url}}
        )
        print(f"Modified {result.modified_count} product with ID: {product_id}")
    except OperationFailure as e:
        print(f"Error updating product: {e}")

def delete_product(db, product_id):
    """Deletes a product from the database."""
    try:
        products_collection = db["products"]
        result = products_collection.delete_one({"product_id": product_id})
        print(f"Deleted {result.deleted_count} product with ID: {product_id}")
    except OperationFailure as e:
        print(f"Error deleting product: {e}")

def get_free_products(db):
    """Retrieves all free products from the database."""
    try:
        products_collection = db["products"]
        free_products = products_collection.find({"price": 0})
        return list(free_products)  # Return a list of product documents
    except OperationFailure as e:
        print(f"Error getting free products: {e}")
        return []

def get_paid_products(db):
    """Retrieves all paid products from the database."""
    try:
        products_collection = db["products"]
        paid_products = products_collection.find({"price": {"$gt": 0}})
        return list(paid_products)  # Return a list of product documents
    except OperationFailure as e:
        print(f"Error getting paid products: {e}")
        return []

# (Implement similar functions for users and orders)

def initialize_database():
    """Initializes the database and creates collections."""
    client = connect_db()
    if client:
        db = client["Flexer_Premium_Shop"]  # Database name from the screenshot
        create_collections(db)
        client.close()

if __name__ == "__main__":
    initialize_database()
        
