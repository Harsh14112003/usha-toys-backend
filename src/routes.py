from typing import Annotated, List
import jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId

from model.authentication import Token, User, UserCreate, TokenRefresh
from model.product import Product, Category, CartItem, WishlistItem, CartItemResponse, WishlistItemResponse
from service.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
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
    remove_from_wishlist
)

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user_in: UserCreate):
    user = create_user(user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
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
    # We can also rotate the refresh token here if we want
    new_refresh_token = create_refresh_token(data={"sub": username})
    return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")


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
