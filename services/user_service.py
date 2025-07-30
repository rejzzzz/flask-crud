from flask import jsonify
from models.user import validate_user_data, hash_password, get_next_user_id
from db import get_db
from utils.response import success_response, error_response
import logging


def get_all_users():

    try:
        collection = get_db()
        users = []
        for user in collection.find({}, {'password': 0}):
            users.append({
                'id': str(user['_id']),
                'user_id': user['user_id'],
                'name': user['name'],
                'email': user['email']
            })
        return success_response(data=users, message="Users retrieved successfully")
    except Exception as e:
        logging.error(f"Error fetching all users: {e}")
        return error_response("Failed to retrieve users", 500)


def get_user_by_id(user_id):

    try:
        collection = get_db()
        user = collection.find_one({'user_id': user_id}, {'password': 0})
        if not user:
            return error_response("User not found", 404)
        return success_response(data={
            'id': str(user['_id']),
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email']
        }, message="User retrieved successfully")
    except Exception as e:
        logging.error(f"Error fetching user {user_id}: {e}")
        return error_response("Internal server error", 500)


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


def delete_user(user_id):

    try:
        collection = get_db()
        result = collection.delete_one({'user_id': user_id})
        if result.deleted_count == 0:
            return error_response("User not found", 404)
        return success_response(message="User deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {e}")
        return error_response("Failed to delete user", 500)