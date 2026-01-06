import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.board import Board
from app.models.card import Card

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(
                    message="Try something new every day", 
                    like_count=0)
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def one_board(app):
    new_board = Board(title="Build a habit of going outside daily",
                      owner="Alice")
    
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def board_with_two_cards(app):
    board = Board(title="Test Board", owner="Madi Rei")
    db.session.add(board)
    db.session.commit()

    card_1 = Card(
        message="A Message",
        like_count=0,
        board_id=board.id
    )
    card_2 = Card(
        message="Another Message",
        like_count=0,
        board_id=board.id
    )

    db.session.add_all([card_1, card_2])
    db.session.commit()

    return board