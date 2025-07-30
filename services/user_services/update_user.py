from models.user import validate_user_data, hash_password
from db import get_db
from utils.response import success_response, error_response
import logging

def update_user(user_id, data):

    validation = validate_user_data(data, is_create=False)
    if not validation['is_valid']:
        return error_response(validation['message'], 400)

    name, email = data['name'], data['email']
    password = data.get('password')

    try:
        collection = get_db()

        user = collection.find_one({'user_id': user_id})
        if not user:
            return error_response("User not found", 404)

        existing_user = collection.find_one({'email': email})
        if existing_user and existing_user['user_id'] != user_id:
            return error_response("Email already in use", 409)

        update_data = {
            'name': name,
            'email': email
        }
        if password:
            update_data['password'] = hash_password(password)

        collection.update_one({'user_id': user_id}, {'$set': update_data})
        return success_response(message="User updated successfully")

    except Exception as e:
        logging.error(f"Error updating user {user_id}: {e}")
        return error_response("Failed to update user", 500)