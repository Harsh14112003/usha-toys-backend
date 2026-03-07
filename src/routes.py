from typing import Annotated, List
import os
import jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import uuid
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId

from model.authentication import Token, User, UserCreate, TokenRefresh
from model.product import Product, Category, CartItem, WishlistItem, CartItemResponse, WishlistItemResponse, Order
from service.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_user,
    create_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_SECRET_KEY,
    ALGORITHM
)
from service.product import (
    get_all_products, 
    get_product_by_id, 
    get_all_categories,
    get_cart,
    add_to_cart,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    get_wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    create_product,
    update_product
)
from service.s3 import upload_file_to_s3
from service.payment import create_razorpay_order, verify_payment

router = APIRouter()

@router.post("/signup")
async def signup(user_in: UserCreate):
    user = create_user(user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    return {"message": "User created successfully. Please check your email to verify your account before logging in."}

@router.get("/verify-email")
async def verify_email_route(token: str):
    from database import get_db
    db = get_db()
    
    user_dict = db.users.find_one({"verification_token": token})
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    db.users.update_one(
        {"_id": user_dict["_id"]},
        {
            "$set": {"is_verified": True},
            "$unset": {"verification_token": ""}
        }
    )
    
    # In a real app, you might want to return an HTML page here,
    # or redirect the user to a frontend success page.
    return {"message": "Email verified successfully! You can now log in."}


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type="bearer",
        user=user
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await login(form_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(token_refresh: TokenRefresh):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token_refresh.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    # Rotate the refresh token
    new_refresh_token = create_refresh_token(data={"sub": username})
    # Look up the user so we can include it in the response (Token model requires it)
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer", user=user)


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@router.get("/products", response_model=List[Product])
async def get_products():
    return get_all_products()


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if product_id == "invalid": # Just for demonstration if needed
         raise HTTPException(status_code=400, detail="Invalid product ID")
    
    if not product:
        # Check if it was invalid ID or just not found
        if not ObjectId.is_valid(product_id):
             raise HTTPException(status_code=400, detail="Invalid product ID")
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.get("/categories", response_model=List[Category])
async def get_categories_route():
    return get_all_categories()


# --- Cart Routes ---

@router.get("/cart", response_model=List[CartItemResponse])
async def get_user_cart_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return get_cart(current_user.username)

@router.post("/cart")
async def add_to_cart_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id: str,
    quantity: int = 1
):
    add_to_cart(current_user.username, product_id, quantity)
    return {"message": "Item added to cart"}

@router.patch("/cart/{product_id}")
async def update_cart_quantity_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id: str,
    quantity: int
):
    update_cart_quantity(current_user.username, product_id, quantity)
    return {"message": "Cart updated"}

@router.delete("/cart/{product_id}")
async def remove_from_cart_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id: str
):
    remove_from_cart(current_user.username, product_id)
    return {"message": "Item removed from cart"}

@router.delete("/cart")
async def clear_cart_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    clear_cart(current_user.username)
    return {"message": "Cart cleared"}


# --- Wishlist Routes ---

@router.get("/wishlist", response_model=List[WishlistItemResponse])
async def get_user_wishlist_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return get_wishlist(current_user.username)

@router.post("/wishlist")
async def add_to_wishlist_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id: str
):
    add_to_wishlist(current_user.username, product_id)
    return {"message": "Item added to wishlist"}

@router.delete("/wishlist/{product_id}")
async def remove_from_wishlist_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id: str
):
    remove_from_wishlist(current_user.username, product_id)
    return {"message": "Item removed from wishlist"}

@router.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    urls = []

    for file in files:
        try:
            # Read file content
            content = await file.read()

            if not content:
                raise HTTPException(status_code=400, detail=f"{file.filename} is empty")

            # Get file extension safely
            filename = file.filename or "file"
            ext = os.path.splitext(filename)[1]

            # Generate unique name
            unique_filename = f"products/{uuid.uuid4()}{ext}"

            # Upload to S3
            url = upload_file_to_s3(
                content,
                unique_filename,
                file.content_type or "application/octet-stream"
            )

            if not url:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload {filename}"
                )

            urls.append(url)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"urls": urls}

@router.post("/products", response_model=Product)
async def add_product_route(
    product: Product,
    # current_user: Annotated[User, Depends(get_current_active_user)], # Add admin check here
):
    # In a real app, check if current_user.is_admin
    new_product = create_product(product)
    return new_product

@router.put("/products/{product_id}", response_model=Product)
async def update_product_route(
    product_id: str,
    product: Product,
    # current_user: Annotated[User, Depends(get_current_active_user)],
):
    updated = update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

# --- Payment Routes ---

@router.post("/payments/create-order", response_model=Order)
async def create_order_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    cart = get_cart(current_user.username)
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    subtotal = sum(item["product"]["price"] * item["quantity"] for item in cart)
    tax = round(subtotal * 0.18)
    shipping = 0 if subtotal > 999 else 99
    total = subtotal + tax + shipping
    
    order = create_razorpay_order(total, current_user.username, cart)
    if not order:
        raise HTTPException(status_code=500, detail="Failed to create Razorpay order")
    
    # Return key_id so frontend doesn't have to hardcode it or use env
    order["razorpay_key_id"] = os.getenv("RAZORPAY_KEY_ID")
    return order

@router.post("/payments/verify")
async def verify_payment_route(
    current_user: Annotated[User, Depends(get_current_active_user)],
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str
):
    success = verify_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature)
    if success:
        clear_cart(current_user.username)
        return {"message": "Payment verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Payment verification failed")

