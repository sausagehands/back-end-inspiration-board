from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(
        back_populates="board",
        cascade="all, delete-orphan")

    def to_dict(self):
        board_as_dict = {
            'id': self.id,
            'title': self.title,
            'owner': self.owner,
            'cards': [card.to_dict() for card in self.cards]
        }

        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = cls(title=board_data["title"], owner=board_data["owner"])
        return new_board
    
