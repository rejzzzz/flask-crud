from flask import Flask, request, jsonify
from config import Config
from db import get_db
from services.user_services.create_user import create_user
from services.user_services.get_all_users import get_all_users
from services.user_services.get_user_by_id import get_user_by_id
from services.user_services.update_user import update_user
from services.user_services.delete_user import delete_user
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        get_db()

    @app.route('/', methods=['GET'])
    def health():
        return jsonify({"status": "healthy", "database": "connected"}), 200

    @app.route('/users/', methods=['GET'])
    def list_users():
        return get_all_users()

    @app.route('/users/<user_id>/', methods=['GET'])
    def get_user(user_id):
        return get_user_by_id(user_id)

    @app.route('/users/', methods=['POST'])
    def add_user():
        data = request.get_json()
        return create_user(data)

    @app.route('/users/<user_id>/', methods=['PUT'])
    def update_user_route(user_id):
        data = request.get_json()
        return update_user(user_id, data)

    @app.route('/users/<user_id>/', methods=['DELETE'])
    def delete_user_route(user_id):
        return delete_user(user_id)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))