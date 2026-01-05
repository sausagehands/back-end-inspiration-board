from flask import Blueprint, make_response, request, Response
from .route_utilities import validate_model, create_model, get_models_with_filters
from app.models.card import Card
from app.models.board import Board
from ..db import db

bp = Blueprint("board_bp",__name__, url_prefix="/boards")
