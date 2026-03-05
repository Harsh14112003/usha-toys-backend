from bson import ObjectId
from database import get_db

def get_all_products():
    db = get_db()
    return list(db.products.find())

def get_product_by_id(product_id: str):
    db = get_db()
    if not ObjectId.is_valid(product_id):
        return None
    return db.products.find_one({"_id": ObjectId(product_id)})

def get_all_categories():
    db = get_db()
    return list(db.categories.find())

def get_cart(user_id: str):
    db = get_db()
    cart_items = list(db.cart.find({"user_id": user_id}))
    enriched_cart = []
    for item in cart_items:
        product = db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            enriched_cart.append({
                "product": product,
                "quantity": item["quantity"]
            })
    return enriched_cart

def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    db = get_db()
    existing_item = db.cart.find_one({"user_id": user_id, "product_id": product_id})
    if existing_item:
        db.cart.update_one(
            {"_id": existing_item["_id"]},
            {"$inc": {"quantity": quantity}}
        )
    else:
        db.cart.insert_one({
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        })

def update_cart_quantity(user_id: str, product_id: str, quantity: int):
    db = get_db()
    db.cart.update_one(
        {"user_id": user_id, "product_id": product_id},
        {"$set": {"quantity": quantity}}
    )

def remove_from_cart(user_id: str, product_id: str):
    db = get_db()
    db.cart.delete_one({"user_id": user_id, "product_id": product_id})

def clear_cart(user_id: str):
    db = get_db()
    db.cart.delete_many({"user_id": user_id})

def get_wishlist(user_id: str):
    db = get_db()
    wishlist_items = list(db.wishlist.find({"user_id": user_id}))
    enriched_wishlist = []
    for item in wishlist_items:
        product = db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            enriched_wishlist.append({
                "product": product
            })
    return enriched_wishlist

def add_to_wishlist(user_id: str, product_id: str):
    db = get_db()
    if not db.wishlist.find_one({"user_id": user_id, "product_id": product_id}):
        db.wishlist.insert_one({
            "user_id": user_id,
            "product_id": product_id
        })

def remove_from_wishlist(user_id: str, product_id: str):
    db = get_db()
    db.wishlist.delete_one({"user_id": user_id, "product_id": product_id})
