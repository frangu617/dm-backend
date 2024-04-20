from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_pymongo import ObjectId, PyMongo

from app import mongo  # make sure mongo is initialized in your main app config

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/', methods=['POST'])
def create_user():
    try:
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        role = request.json.get('role', 'user')

        hashed_password = generate_password_hash(password)
        
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,  # store hashed password
            "role": role
        }
        result = mongo.db.users.insert_one(user_data)
        user_data['id'] = str(result.inserted_id)  # convert ObjectId to string
        del user_data['password']  # remove password hash from response

        return jsonify(message="User created successfully", user=user_data), 201
    except Exception as e:  # catch all exceptions for simplicity
        return jsonify(error=str(e)), 400

@users_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({"_id": ObjectId(current_user_id)})
    if current_user and current_user.get("role") != "admin":
        return jsonify(error="Unauthorized: Insufficient permissions"), 403

    users = list(mongo.db.users.find({}, {'password': 0}))  # exclude password from the results
    return jsonify(users=users), 200

@users_blueprint.route('/current', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(current_user_id)}, {'password': 0})
    if user:
        return jsonify(user), 200
    else:
        return jsonify(error="Unauthorized: No current user"), 401
