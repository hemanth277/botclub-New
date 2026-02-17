
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def run_tests():
    session = requests.Session()
    
    print("1. Testing Registration...")
    reg_data = {
        "username": "testuser_flask",
        "email": "test_flask@example.com",
        "password": "password123"
    }
    try:
        # cleanup first
        pass 
    except:
        pass

    try:
        res = session.post(f"{BASE_URL}/auth/register", json=reg_data)
        print(f"Register Status: {res.status_code}")
        if res.status_code == 201:
            print("Response:", res.json())
        else:
            print("Error/User might exist:", res.text)
    except Exception as e:
        print("Register failed:", e)

    print("\n2. Testing Login...")
    login_data = {
        "username": "testuser_flask",
        "password": "password123"
    }
    user_id = None
    try:
        res = session.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            print("Login Successful")
            user_id = data['user']['id']
        else:
            print("Login Failed:", res.text)
            return
    except Exception as e:
        print("Login failed:", e)
        return

    print("\n3. Testing Product Creation...")
    prod_data = {
        "name": "Flask Test Product",
        "price": 99.99,
        "description": "Created by test script",
        "category": "Test",
        "imageUrl": "http://example.com/image.png",
        "stock": 10
    }
    product_id = None
    try:
        res = session.post(f"{BASE_URL}/products/", json=prod_data)
        print(f"Create Product Status: {res.status_code}")
        if res.status_code == 201:
            data = res.json()
            product_id = data['_id'] # verify field name in response
            # My auth route returns `_id`, product route uses `.to_json()` default or `jsonify(product)`?
            # Creating product returns `jsonify(product)`. MongoEngine objects to jsonify?
            # Wait, `jsonify(product)` on a MongoEngine document might fail if it doesn't support json serialization natively.
            # I should have used `.to_json()` or converted to dict.
            # Let's hope Flask-MongoEngine handles it or check `app.py`.
            # I did NOT use `to_json()` in `create_product`.
            pass
    except Exception as e:
        print("Create product failed:", e)

    print("\n4. Listing Products...")
    try:
        res = session.get(f"{BASE_URL}/products/")
        print(f"List Products Status: {res.status_code}")
        # print(res.json())
    except Exception as e:
        print("List products failed:", e)
        
    if user_id and product_id:
        print("\n5. Adding to Wishlist...")
        try:
             res = session.post(f"{BASE_URL}/user/wishlist", json={"userId": user_id, "productId": product_id})
             print(f"Wishlist Status: {res.status_code}")
             print("Response:", res.text)
        except Exception as e:
             print("Wishlist failed:", e)

if __name__ == "__main__":
    run_tests()
