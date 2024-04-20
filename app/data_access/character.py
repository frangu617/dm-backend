from flask import current_app as app
from bson.objectid import ObjectId
from datetime import datetime

def create_character(data):
    """
    Create a new character in the database.
    Expects 'data' to include 'name', 'race', 'class', 'level', etc.
    """
    # Assuming 'user' is passed as an ObjectId string and needs to be converted
    data['user'] = ObjectId(data['user'])  
    data['created_at'] = datetime.utcnow()
    result = app.mongo.db.characters.insert_one(data)
    return result.inserted_id  # Returns the ObjectId of the newly created character

def get_character(character_id):
    """
    Retrieve a character by its ObjectId.
    """
    return app.mongo.db.characters.find_one({"_id": ObjectId(character_id)})

def update_character(character_id, update_data):
    """
    Update an existing character's data.
    """
    # Ensure updates don't unintentionally change the user associated
    if 'user' in update_data:
        update_data['user'] = ObjectId(update_data['user'])
    result = app.mongo.db.characters.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": update_data}
    )
    return result.modified_count  # Returns the count of documents modified

def delete_character(character_id):
    """
    Delete a character by its ObjectId.
    """
    result = app.mongo.db.characters.delete_one({"_id": ObjectId(character_id)})
    return result.deleted_count  # Returns the count of documents deleted

def list_characters_by_user(user_id):
    """
    List all characters belonging to a specific user.
    """
    return list(app.mongo.db.characters.find({"user": ObjectId(user_id)}))
