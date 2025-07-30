from models.user import validate_user_data, hash_password, get_next_user_id
from db import get_db
from utils.response import success_response, error_response
import logging

def create_user(data):

    validation = validate_user_data(data, is_create=True)
    if not validation['is_valid']:
        return error_response(validation['message'], 400)

    name, email, password = data['name'], data['email'], data['password']

    try:
        collection = get_db()

        if collection.find_one({'email': email}):
            return error_response("Email already in use", 409)

        try:
            user_id = get_next_user_id()
        except RuntimeError as e:
            return error_response(str(e), 503)

        hashed_pw = hash_password(password)

        result = collection.insert_one({
            'user_id': user_id,
            'name': name,
            'email': email,
            'password': hashed_pw
        })

        return success_response(
            data={
                'id': str(result.inserted_id),
                'user_id': user_id,
                'name': name,
                'email': email
            },
            message="User created successfully",
            status=201
        )

    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return error_response("Failed to create user", 500)