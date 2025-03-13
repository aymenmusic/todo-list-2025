from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()  # Database ORM
jwt = JWTManager()  # JSON Web Token manager for authentication
migrate = Migrate()  # Database migration tool


def create_app():
    """
    Application factory function that creates and configures the Flask app
    This pattern allows for easier testing and multiple instances
    """
    app = Flask(__name__)

    # Configure the app from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    # Disable modification tracking to improve performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # Set JWT token location to headers only
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    # Set JWT header type to Bearer
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    # Initialize extensions with the app
    db.init_app(app)  # Connect SQLAlchemy to Flask
    jwt.init_app(app)  # Connect JWT manager to Flask
    migrate.init_app(app, db)  # Connect migration tool to Flask and SQLAlchemy
    CORS(app)  # Enable Cross-Origin Resource Sharing for API requests from frontend

    # Register error handlers for JWT exceptions
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid token',
            'message': str(error)
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({
            'error': 'Missing Authorization Header',
            'message': str(error)
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'message': 'Please log in again'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has been revoked',
            'message': 'Please log in again'
        }), 401

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error for debugging
        app.logger.error(f"Unhandled exception: {str(e)}")

        # Return a generic error message
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

    # Add a route for the root path
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the Todo List API',
            'endpoints': {
                'auth': '/api/auth',
                'todos': '/api/todos'
            },
            'documentation': 'See README.md for API documentation'
        })

    # Import blueprints (we'll create these files next)
    # Blueprints are a way to organize related routes
    from app.routes.auth import auth_bp
    from app.routes.todos import todos_bp

    # Register blueprints with URL prefixes
    # This means auth routes will start with /api/auth and todo routes with /api/todos
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')

    # Return the configured app
    return app
