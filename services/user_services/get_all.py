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