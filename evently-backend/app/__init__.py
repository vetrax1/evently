from flask import Flask
from flask_cors import CORS
from .db import db
from .routes import api_blueprint
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    # Enable CORS
    CORS(app)  # <--- THIS is the fix

    # Init DB
    db.init_app(app)

    # Register API
    app.register_blueprint(api_blueprint)

    with app.app_context():
        db.create_all()

    return app
