import razorpay
import os
from dotenv import load_dotenv
from database import get_db
from datetime import datetime
from bson import ObjectId
from model.product import Order

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_razorpay_order(amount: float, user_id: str, items: list):
    """
    Creates a Razorpay order and stores it in the database.
    Amount should be in INR (not subunits here, we convert to subunits for Razorpay).
    """
    db = get_db()
    
    # Razorpay expects amount in paise (subunits)
    razorpay_order_data = {
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1 # Auto capture
    }
    
    try:
        razorpay_order = client.order.create(data=razorpay_order_data)
        
        now = datetime.now()
        order_dict = {
            "user_id": user_id,
            "amount": amount,
            "currency": "INR",
            "razorpay_order_id": razorpay_order["id"],
            "status": "created",
            "items": items,
            "dateCreated": now,
            "dateModified": now
        }
        
        db.orders.insert_one(order_dict)
        return order_dict
    except Exception as e:
        print(f"Error creating Razorpay order: {e}")
        return None

def verify_payment(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str):
    """
    Verifies the Razorpay payment signature and updates order status.
    """
    db = get_db()
    
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    
    try:
        client.utility.verify_payment_signature(params_dict)
        
        db.orders.update_one(
            {"razorpay_order_id": razorpay_order_id},
            {"$set": {
                "status": "paid",
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
                "dateModified": datetime.now()
            }}
        )
        return True
    except Exception as e:
        print(f"Payment verification failed: {e}")
        db.orders.update_one(
            {"razorpay_order_id": razorpay_order_id},
            {"$set": {
                "status": "failed",
                "dateModified": datetime.now()
            }}
        )
        return False
