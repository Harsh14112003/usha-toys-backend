import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    print("Testing Signup...")
    signup_data = {
        "username": "testuser_cart",
        "email": "test_cart@example.com",
        "password": "password123",
        "full_name": "Cart Tester"
    }
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    if response.status_code == 200:
        print("Signup successful")
        return response.json()
    else:
        print(f"Signup failed: {response.text}")
        # Try login if already exists
        login_data = {"username": "testuser_cart", "password": "password123"}
        response = requests.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200:
            print("Login successful")
            return response.json()
        else:
            print(f"Login failed: {response.text}")
            return None

def test_cart_wishlist(auth_data):
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get Product ID
    print("\nFetching products...")
    resp = requests.get(f"{BASE_URL}/products")
    products = resp.json()
    if not products:
        print("No products available to test")
        return
    product_id = str(products[0]["_id"])
    print(f"Using product_id: {product_id}")

    # 2. Add to Cart
    print("\nAdding to cart...")
    resp = requests.post(f"{BASE_URL}/cart?product_id={product_id}&quantity=2", headers=headers)
    print(f"Add to cart: {resp.status_code} - {resp.text}")

    # 3. Get Cart
    print("\nGetting cart...")
    resp = requests.get(f"{BASE_URL}/cart", headers=headers)
    print(f"Get cart status: {resp.status_code}")
    try:
        print(f"Get cart info: {resp.json()}")
    except Exception as e:
        print(f"Get cart failed to parse JSON: {e}")
        print(f"Response text: {resp.text}")

    # 4. Add to Wishlist
    print("\nAdding to wishlist...")
    resp = requests.post(f"{BASE_URL}/wishlist?product_id={product_id}", headers=headers)
    print(f"Add to wishlist: {resp.status_code} - {resp.text}")

    # 5. Get Wishlist
    print("\nGetting wishlist...")
    resp = requests.get(f"{BASE_URL}/wishlist", headers=headers)
    print(f"Get wishlist: {resp.status_code} - {resp.json()}")

if __name__ == "__main__":
    auth = test_auth()
    if auth:
        test_cart_wishlist(auth)
