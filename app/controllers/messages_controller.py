from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data_access.message import create_message, get_messages_by_user, get_message, delete_message

messages_blueprint = Blueprint('messages', __name__)

@messages_blueprint.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    from_user = get_jwt_identity()
    to_user = request.json.get('toUser')
    message_text = request.json.get('message')
    message_id = create_message(from_user, to_user, message_text)
    return jsonify({"message_id": str(message_id)}), 201

@messages_blueprint.route('/messages', methods=['GET'])
@jwt_required()
def user_messages():
    user_id = get_jwt_identity()
    messages = get_messages_by_user(user_id)
    return jsonify(messages), 200

@messages_blueprint.route('/messages/<message_id>', methods=['GET'])
@jwt_required()
def message_details(message_id):
    message = get_message(message_id)
    if message:
        return jsonify(message), 200
    else:
        return jsonify({"error": "Message not found"}), 404

@messages_blueprint.route('/messages/<message_id>', methods=['DELETE'])
@jwt_required()
def delete_message_route(message_id):
    count = delete_message(message_id)
    if count:
        return jsonify({"message": "Deleted successfully"}), 204
    else:
        return jsonify({"error": "Message not found"}), 404
