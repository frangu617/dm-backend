from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import mongo

def create_user(username, email, password, role="user"):
    """
    Create a new user in the database.
    """
    hashed_password = generate_password_hash(password)
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "role": role
    }
    result = app.mongo.db.users.insert_one(user_data)
    return result.inserted_id  # Returns the ObjectId of the newly created user

def find_user_by_id(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        user['id'] = str(user['_id'])  # convert ObjectId to string
        del user['_id']  # remove the MongoDB-specific ID if desired
    return user

def find_user_by_username(username):
    """
    Find a user by their username.
    """
    return app.mongo.db.users.find_one({"username": username})

def check_user_password(user_id, password):
    """
    Check if the provided password matches the stored password hash.
    """
    user = find_user_by_id(user_id)
    if user and check_password_hash(user['password'], password):
        return True
    return False

def update_user(user_id, update_data):
    """
    Update a user's information.
    """
    if 'password' in update_data:  # If updating the password, hash it
        update_data['password'] = generate_password_hash(update_data['password'])
    result = app.mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return result.modified_count

def delete_user(user_id):
    """
    Delete a user by their ObjectId.
    """
    result = app.mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count
