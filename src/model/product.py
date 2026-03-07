from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime
from bson import ObjectId

# Custom type to convert ObjectId to string
PyObjectId = Annotated[str, BeforeValidator(str)]

class Category(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    icon: str
    count: int
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None

    class Config:
        populate_by_name = True

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    description: str
    price: float
    originalPrice: Optional[float] = None
    category: str
    ageGroup: str
    image: str
    images: List[str]
    rating: float
    reviewCount: int
    inStock: bool
    featured: bool
    badge: Optional[str] = None
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None

    class Config:
        populate_by_name = True

class CartItem(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    user_id: str
    product_id: str
    quantity: int = 1
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None

    class Config:
        populate_by_name = True

class WishlistItem(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    user_id: str
    product_id: str
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None

    class Config:
        populate_by_name = True

class CartItemResponse(BaseModel):
    product: Product
    quantity: int

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    user_id: str
    amount: float
    currency: str = "INR"
    razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None
    status: str = "created"  # created, paid, failed
    items: List[CartItemResponse]
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    razorpay_key_id: Optional[str] = None

    class Config:
        populate_by_name = True

class WishlistItemResponse(BaseModel):
    product: Product
