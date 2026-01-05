from flask import Blueprint, make_response, request, Response
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

@bp.post("/<board_id>/card")
def create_card(board_id):
    # TODO: Check for board existence
    request_body = request.get_json()
    message = request_body.get("message")

    if not message or not isinstance(message, str) or message.strip() == "":
        return make_response({"details": "Invalid data: message cannot be empty"}, 400)

    if len(message) > 40:
        return make_response({"details": "Invalid data: message must be 40 characters or fewer"}, 400)

    try:
        new_card = Card.from_dict(request_body)
        new_card.board_id = int(board_id)

    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_card)
    db.session.commit()

    return make_response({"id": new_card.id, "message": new_card.message}, 201)

# READ
@bp.get("")
def get_all_boards():
    return get_models_with_filters(Board, request.args)

@bp.get("/<board_id>")
def get_board_by_id(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict()

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