from db import get_db
from utils.response import success_response, error_response
import logging

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