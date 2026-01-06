from flask import Blueprint, make_response, request, Response, abort
from .route_utilities import validate_model, create_model, get_models_with_filters
from app.models.card import Card
from app.models.board import Board
from ..db import db

bp = Blueprint("board_bp",__name__, url_prefix="/boards")

# CREATE
@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)
    

@bp.post("/<board_id>/cards")
def create_card(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    if not request_body or "message" not in request_body:
        abort(make_response(
            {"details": "Invalid request: missing message"},
            400
        ))

    message = request_body["message"]

    if not isinstance(message, str) or message.strip() == "":
        abort(make_response(
            {"details": "Invalid data: message cannot be empty"},
            400
        ))

    if len(message) > 40:
        abort(make_response(
            {"details": "Invalid data: message must be 40 characters or fewer"},
            400
        ))

    new_card = Card.from_dict({
        "message": message,
        "board_id": board.id
    })

    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201

# READ
@bp.get("")
def get_all_boards():
    return get_models_with_filters(Board, request.args)

@bp.get("/<board_id>")
def get_board_by_id(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict()

@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    
    cards_response = [card.to_dict() for card in board.cards]
    
    return cards_response

# UPDATE
@bp.put("/<board_id>")
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    if "title" in request_body:
        board.title = request_body["title"]
    if "owner" in request_body:
        board.owner = request_body["owner"]
        
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE
@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()

    return Response(status=204, mimetype="application/json")