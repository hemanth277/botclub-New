from flask import Blueprint, request, jsonify
from models.user import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password.decode('utf-8'),
            role=data.get('role', 'customer')
        )
        user.save()
        
        # Convert to dict to avoid serialization issues with MongoEngine object
        user_dict = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "_id": str(user.id)
        }
        return jsonify(user_dict), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.objects(username=data['username']).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 400
            
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"message": "Invalid password"}), 400
            
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "role": user.role
            }
        })
    except Exception as e:
        return jsonify({"message": str(e)}), 500
