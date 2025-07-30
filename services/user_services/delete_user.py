from db import get_db
from utils.response import success_response, error_response
import logging

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