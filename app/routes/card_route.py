from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import validate_model
from app.models.card import Card
from app.models.board import Board
from ..db import db
bp = Blueprint("card_bp",__name__, url_prefix="/cards")

# Create a card
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

    
# Update a card's like count
@bp.patch("/<id>/like")
def like_card(id):
    try:
        card_id = int(id)
    except:
        response = {"details": f"Card {id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Card).where(Card.id == card_id)
    card = db.session.scalar(query)

    if not card:
        response = {"details": f"Card {id} not found"}
        abort(make_response(response, 404))

    card.like_count += 1
    db.session.commit()
    return make_response({"id": card.id, "message": card.message, "like_count": card.like_count}, 200)


# Read all cards
@bp.get("")
def get_all_cards():
    query = db.select(Card)
    cards = db.session.scalars(query.order_by(Card.id))
    cards_response = []
    for card in cards:
        cards_response.append(
            {
                "id": card.id,
                "message": card.message,
                "like_count": card.like_count
            }
        )
    return cards_response


# Delete a card
@bp.delete("/<id>")
def delete_card(id):
    card = validate_model(Card,id)
    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

