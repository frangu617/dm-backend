from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId  # For handling ObjectId in PyMongo
from app.data_access.user import create_user, find_user_by_username, check_user_password


# Assuming mongo is initialized elsewhere and imported here
from app import mongo

authentication_blueprint = Blueprint('authentication', __name__)

@authentication_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    user_id = create_user(username, email, password)
    return jsonify({"user_id": str(user_id)}), 201

@authentication_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = find_user_by_username(username)
    if user and check_user_password(user['_id'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(error="Invalid credentials"), 401
