from flask import Flask
from config import Config
from db import get_db
from routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        get_db()

    # Register all route blueprints
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
