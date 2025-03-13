from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db
import datetime

# Create a Blueprint for authentication routes
# Blueprints are a way to organize related routes
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    Request body:
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepassword"
    }
    """
    # Get data from request
    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    # Save user to database
    db.session.add(user)
    db.session.commit()

    # Return success response
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user
    ---
    Request body:
    {
        "username": "johndoe",
        "password": "securepassword"
    }
    """
    # Get data from request
    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Find user by username
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Create access token with expiration
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        # Convert user.id to string to avoid JWT subject error
        identity=str(user.id),
        expires_delta=expires
    )

    # Return token and user info
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    ---
    Requires JWT token in Authorization header
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()

    # Find user by ID (convert string ID back to integer if needed)
    user = User.query.get(
        int(user_id) if isinstance(user_id, str) else user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Return user info
    return jsonify(user.to_dict()), 200
