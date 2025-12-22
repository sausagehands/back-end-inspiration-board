from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'card_ids': [card.id for card in self.cards],
            'cards': [ card.to_dict() for card in self.cards]
        }

    def to_summary_dict(self):
        dictionary = {"id": self.id, "message": self.message}
        return dictionary

    @classmethod
    def from_dict(cls, dict_data: dict):
        board = Board(
            id=dict_data.get("id"),
            message=dict_data["message"],
        )
        return board
    