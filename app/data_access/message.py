from flask import current_app as app
from bson.objectid import ObjectId
from datetime import datetime

def create_message(from_user_id, to_user_id, message_text):
    """Create a new message in the MongoDB collection."""
    message_data = {
        "from_user": ObjectId(from_user_id),
        "to_user": ObjectId(to_user_id),
        "message": message_text,
        "created_at": datetime.utcnow()
    }
    result = app.mongo.db.messages.insert_one(message_data)
    return result.inserted_id  # Returns the ObjectId of the newly created message

def get_messages_by_user(user_id):
    """Retrieve all messages sent to or from a specific user."""
    messages = app.mongo.db.messages.find({
        "$or": [{"from_user": ObjectId(user_id)}, {"to_user": ObjectId(user_id)}]
    }).sort("created_at", -1)  # Sorting by date descending
    return list(messages)

def get_message(message_id):
    """Retrieve a specific message by its ID."""
    message = app.mongo.db.messages.find_one({"_id": ObjectId(message_id)})
    return message

def delete_message(message_id):
    """Delete a specific message by its ID."""
    result = app.mongo.db.messages.delete_one({"_id": ObjectId(message_id)})
    return result.deleted_count
