from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data_access.character import create_character, get_character, update_character, delete_character, list_characters_by_user

character_blueprint = Blueprint('character', __name__)

@character_blueprint.route('/characters', methods=['POST'])
@jwt_required()
def add_character():
    user_id = get_jwt_identity()
    data = request.get_json()
    data['user'] = user_id  # Ensure user ID is included
    character_id = create_character(data)
    return jsonify({"message": "Character created successfully", "character_id": str(character_id)}), 201

@character_blueprint.route('/characters/<character_id>', methods=['GET'])
@jwt_required()
def character_details(character_id):
    character = get_character(character_id)
    if character:
        return jsonify(character), 200
    else:
        return jsonify({"error": "Character not found"}), 404

@character_blueprint.route('/characters/<character_id>', methods=['PUT'])
@jwt_required()
def character_update(character_id):
    data = request.get_json()
    modified_count = update_character(character_id, data)
    if modified_count:
        return jsonify({"message": "Character updated successfully"}), 200
    else:
        return jsonify({"error": "Update failed or no changes made"}), 400

@character_blueprint.route('/characters/<character_id>', methods=['DELETE'])
@jwt_required()
def character_delete(character_id):
    deleted_count = delete_character(character_id)
    if deleted_count:
        return jsonify({"message": "Character deleted successfully"}), 204
    else:
        return jsonify({"error": "Character not found"}), 404

@character_blueprint.route('/characters/user', methods=['GET'])
@jwt_required()
def characters_by_user():
    user_id = get_jwt_identity()
    characters = list_characters_by_user(user_id)
    return jsonify(characters), 200
