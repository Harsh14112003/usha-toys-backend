import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    print("Testing Signup...")
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_login():
    print("\nTesting Login...")
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    # FastAPI OAuth2PasswordRequestForm uses form data
    response = requests.post(f"{BASE_URL}/login", data=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_get_me(token):
    print("\nTesting GET /users/me/...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_refresh(refresh_token):
    print("\nTesting Refresh Token...")
    payload = {"refresh_token": refresh_token}
    response = requests.post(f"{BASE_URL}/refresh", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_products():
    print("\nTesting GET /products...")
    response = requests.get(f"{BASE_URL}/products")
    print(f"Status Code: {response.status_code}")
    products = response.json()
    print(f"Retrieved {len(products)} products")
    if products:
        return products[0].get("_id") # Or whatever field we have
    return None

def test_categories():
    print("\nTesting GET /categories...")
    response = requests.get(f"{BASE_URL}/categories")
    print(f"Status Code: {response.status_code}")
    categories = response.json()
    print(f"Retrieved {len(categories)} categories")
    return len(categories) > 0

if __name__ == "__main__":
    # Note: Ensure the server is running before running this test
    # test_products()
    # test_categories()
    # token_data = test_login() # Assuming a user exists
    # if token_data:
    #     new_token = test_refresh(token_data['refresh_token'])
    print("Verification script updated. Please ensure the server is running.")
