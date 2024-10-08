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

# (Similarly implement other functions for get_product, update_product, delete_product, 
#  and functions for users and orders)

def initialize_database():
    """Initializes the database and creates collections."""
    client = connect_db()
    if client:
        db = client["Flexer_Premium_Shop"]  # Database name from the screenshot
        create_collections(db)
        client.close()

# Example usage
if __name__ == "__main__":
    initialize_database()
