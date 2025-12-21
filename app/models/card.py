from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    like_count: Mapped[int] = mapped_column(default=0)
    board_id: Mapped[int | None] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'like_count': self.like_count
        }
        if self.board_id:
            data['board_id'] = self.board_id
        return data

    @classmethod
    def from_dict(cls, dict_data: dict):
        card = Card(
            id=dict_data.get("id"),
            title=dict_data["title"],
            like_count=dict_data.get("like_count", 0)
        )
        return card
    