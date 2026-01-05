from flask import Flask
from flask_cors import CORS
import os
from app.routes.card_route import bp as card_bp
from app.routes.board_route import bp as board_bp
from .db import db, migrate
from .models.card import Card
from .models.board import Board


def create_app(config=None):
    app = Flask(__name__)

    # Register Blueprints here
    app.register_blueprint(card_bp)
    app.register_blueprint(board_bp)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)


    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app
