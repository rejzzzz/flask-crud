from flask import Blueprint, request, jsonify
from services.user_services.create_user import create_user
from services.user_services.get_all_users import get_all_users
from services.user_services.get_user_by_id import get_user_by_id
from services.user_services.update_user import update_user
from services.user_services.delete_user import delete_user

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "connected"}), 200

@user_bp.route('/users/', methods=['GET'])
def list_users():
    return get_all_users()

@user_bp.route('/users/<user_id>/', methods=['GET'])
def get_user(user_id):
    return get_user_by_id(user_id)

@user_bp.route('/users/', methods=['POST'])
def add_user():
    data = request.get_json()
    return create_user(data)

@user_bp.route('/users/<user_id>/', methods=['PUT'])
def update_user_route(user_id):
    data = request.get_json()
    return update_user(user_id, data)

@user_bp.route('/users/<user_id>/', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)
