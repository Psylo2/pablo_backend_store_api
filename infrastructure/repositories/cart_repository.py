from sqlalchemy.ext.mutable import MutableList

from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class CartRepository(db.Model, RepositoryInterface):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    items = db.Column(MutableList.as_mutable(db.PickleType), nullable=False, default=[])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.Float)
    last_modified = db.Column(db.Float)
    user = db.relationship('UserRepository')

    def __init__(self, items: list, user_id: int, created_at: float,
                 last_modified: float, id: int | None = None):
        self.id = id
        self.items = items
        self.user_id = user_id
        self.created_at = created_at
        self.last_modified = last_modified

    def add_to_repository(self) -> None:
        db.session.add(self)
        self.update_repository()

    def remove_from_repository(self) -> None:
        db.session.delete(self)
        self.update_repository()

    def update_repository(self) -> None:
        db.session.commit()

    def to_dict(self) -> dict:
        return {"id": self.id,
                "items": self.items,
                "user_id": self.user_id,
                "created_at": self.created_at,
                "last_modified": self.last_modified}
