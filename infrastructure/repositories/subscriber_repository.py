from uuid import uuid4

from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class SubscriberRepository(db.Model, RepositoryInterface):
    __tablename__ = 'subscribers'
    id = db.Column(db.String(50), primary_key=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String, nullable=False)
    confirm_timestamp = db.Column(db.Float)
    last_ad_sent_timestamp = db.Column(db.Float, nullable=True)

    def __init__(self, email: str):
        self.email = email
        self.id = uuid4().hex
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
                "confirmed": self.confirmed}
