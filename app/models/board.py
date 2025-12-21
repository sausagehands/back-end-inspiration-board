from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'card_ids': [card.id for card in self.cards],
            'cards': [ card.to_dict() for card in self.cards]
        }

    def to_summary_dict(self):
        dictionary = {"id": self.id, "title": self.title}
        return dictionary

    @classmethod
    def from_dict(cls, dict_data: dict):
        board = Board(
            id=dict_data.get("id"),
            title=dict_data["title"],
        )
        return board
    