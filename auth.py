from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# REGISTER route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 400

    # Create and store new user
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# LOGIN route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
