import os
from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/e-commerce')

    # Initialize extensions
    CORS(app)
    
    # Connect to MongoDB
    connect(host=mongodb_uri)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.product import product_bp
    from routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
