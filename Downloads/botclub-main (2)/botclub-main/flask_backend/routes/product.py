from flask import Blueprint, request, jsonify
from models.product import Product
from mongoengine import DoesNotExist, ValidationError
import json

product_bp = Blueprint('products', __name__)

def product_to_dict(product):
    return {
        "_id": str(product.id),
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "imageUrl": product.imageUrl,
        "stock": product.stock
    }

# Get all products
@product_bp.route('/', methods=['GET'])
def get_products():
    try:
        products = Product.objects()
        return jsonify([product_to_dict(p) for p in products]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Delete ALL products
@product_bp.route('/', methods=['DELETE'])
def delete_all_products():
    print("DELETE ALL request received")
    try:
        count = Product.objects.count()
        Product.objects.delete()
        print(f"Deleted {count} products")
        return jsonify({"message": f"Deleted {count} products"}), 200
    except Exception as e:
        print(f"Error deleting all products: {e}")
        return jsonify({"message": f"Server Error: {str(e)}"}), 500

# Add a new product
@product_bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            category=data.get('category'),
            imageUrl=data.get('imageUrl'),
            stock=data.get('stock', 0)
        )
        product.save()
        return jsonify(product_to_dict(product)), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Update a product
@product_bp.route('/<id>', methods=['PUT'])
def update_product(id):
    print("PUT request received for ID:", id)
    print("Request Body:", request.get_json())
    try:
        data = request.get_json()
        product = Product.objects.get(id=id)
        
        # update fields manually or iterate
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        product.save()
        print("Product updated successfully:", product.to_json())
        return jsonify(product_to_dict(product)), 200
    except DoesNotExist:
        print("Product not found with ID:", id)
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print("Error updating product:", e)
        return jsonify({"message": f"Server Error: {str(e)}"}), 500

# Delete a product
@product_bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    print("DELETE request received for ID:", id)
    try:
        product = Product.objects.get(id=id)
        product.delete()
        print("Product deleted:", id)
        return jsonify({"message": "Product deleted"}), 200
    except DoesNotExist:
        print("Product not found for deletion:", id)
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        print("Error deleting product:", e)
        return jsonify({"message": f"Server Error: {str(e)}"}), 500
