from flask import Blueprint, request, jsonify
from models.user import User, CartItem
from models.product import Product
from mongoengine import DoesNotExist

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('userId')
    try:
        user = User.objects.get(id=user_id)
        
        # Manually populate to ensure we return clean JSON and handle missing refs
        wishlist_data = []
        for p in user.wishlist:
            if p: # Check if reference exists
                 wishlist_data.append({
                     "_id": str(p.id),
                     "name": p.name,
                     "price": p.price,
                     "imageUrl": p.imageUrl,
                     "category": p.category,
                     "description": p.description,
                     "stock": p.stock
                 })

        cart_data = []
        for item in user.cart:
            if item.product:
                cart_data.append({
                    "product": {
                        "_id": str(item.product.id),
                        "name": item.product.name,
                        "price": item.product.price,
                        "imageUrl": item.product.imageUrl
                    },
                    "quantity": item.quantity
                })

        user_data = {
            "_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "wishlist": wishlist_data,
            "cart": cart_data
        }
        
        return jsonify(user_data), 200
    except DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_bp.route('/wishlist', methods=['POST'])
def add_wishlist():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        
        # Check if already in wishlist
        if product not in user.wishlist:
            user.update(push__wishlist=product)
            user.reload()
            
        # Return updated wishlist IDs or objects? Node returns array of IDs usually or populated?
        # Node implementation: returns user.wishlist (which was populated in GET but here it might be just IDs if not populated)
        # But for consistency let's return the list of IDs or Objects. 
        # The Node code re-saves and returns `res.json(user.wishlist)`.
        # If we pushed, we should probably return the updated list.
        
        wishlist_ids = [str(p.id) for p in user.wishlist]
        return jsonify(wishlist_ids), 200
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_bp.route('/wishlist', methods=['DELETE'])
def remove_wishlist():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        
        user.update(pull__wishlist=product)
        user.reload()
        
        wishlist_ids = [str(p.id) for p in user.wishlist]
        return jsonify(wishlist_ids), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_bp.route('/cart', methods=['POST'])
def add_cart():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        
        # Check if product in cart
        found = False
        for item in user.cart:
            if str(item.product.id) == product_id:
                item.quantity += 1
                found = True
                break
        
        if not found:
            item = CartItem(product=product, quantity=1)
            user.cart.append(item)
            
        user.save()
        
        # Return cart
        # We need to serialize it
        cart_data = []
        for item in user.cart:
            if item.product:
                 cart_data.append({
                    "product": str(item.product.id), # Node might return full object or ID? 
                    # Node `await user.populate('cart.product')` returns full object.
                     "quantity": item.quantity
                })
        # Wait, if node returns full object, the frontend likely expects full object.
        # Let's try to return full object structure as best effort or just ID if simple.
        # Node response: `res.json(user.cart)` after populate. 
        
        cart_data_populated = []
        for item in user.cart:
             if item.product:
                cart_data_populated.append({
                    "product": {
                        "_id": str(item.product.id),
                        "name": item.product.name,
                        "price": item.product.price,
                        "imageUrl": item.product.imageUrl
                    },
                    "quantity": item.quantity
                })
        
        return jsonify(cart_data_populated), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@user_bp.route('/cart', methods=['DELETE'])
def remove_cart():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    
    try:
        user = User.objects.get(id=user_id)
        
        # Filter out the product
        user.cart = [item for item in user.cart if str(item.product.id) != product_id]
        user.save()
        
        cart_data_populated = []
        for item in user.cart:
             if item.product:
                cart_data_populated.append({
                    "product": {
                        "_id": str(item.product.id),
                        "name": item.product.name,
                        "price": item.product.price,
                        "imageUrl": item.product.imageUrl
                    },
                    "quantity": item.quantity
                })

        return jsonify(cart_data_populated), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
