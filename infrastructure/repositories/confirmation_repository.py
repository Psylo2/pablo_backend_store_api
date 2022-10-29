import os
from time import time, localtime, asctime
from uuid import uuid4

from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class ConfirmationRepository(db.Model, RepositoryInterface):
    __tablename__ = 'confirmation'
    id = db.Column(db.String(50), primary_key=True, nullable=False)
    expired_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    confirm_timestamp = db.Column(db.Float)
    user = db.relationship('UserRepository')

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.id = uuid4().hex
        self.expired_at = int(time()) + int(os.environ.get('CONFIRMATION_EXP_DELTA'))
        self.confirmed = False

    def add_to_repository(self) -> None:
        db.session.add(self)
        self.update_repository()

    def remove_from_repository(self) -> None:
        db.session.delete(self)
        self.update_repository()

    def update_repository(self) -> None:
        db.session.commit()

    def to_dict(self) -> dict:
        return {"confirmation_id": self.id,
                "expired_at": asctime(localtime(self.expired_at)),
                "confirmed": self.confirmed}

    def force_to_expired(self) -> None:
        if not self.expired:
            self.expired_at = int(time())
            self.update_repository()
