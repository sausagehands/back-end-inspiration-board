from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import validate_model
from app.models.card import Card
from app.models.board import Board
from ..db import db
bp = Blueprint("card_bp",__name__, url_prefix="/cards")

# # Update a card's like count
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

#Update a card's message
@bp.put("/<id>")
def update_card(id):
    card = validate_model(Card, id)
    request_body = request.get_json()

    if "message" not in request_body:
        response = {"details": "Invalid request: missing message"}
        return abort(make_response(response, 400))

    card.message = request_body["message"]
    db.session.commit()
    print(card.to_dict())
    return make_response(card.to_dict(), 200)

# Delete a card
@bp.delete("/<id>")
def delete_card(id):
    card = validate_model(Card,id)
    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

