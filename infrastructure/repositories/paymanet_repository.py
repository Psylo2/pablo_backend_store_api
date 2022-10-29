from sqlalchemy.ext.mutable import MutableList

from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class PaymentRepository(db.Model, RepositoryInterface):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    payment_at = db.Column(db.Float, nullable=False)
    state = db.Column(db.Integer, nullable=True)
    transaction_id = db.Column(db.String, nullable=True)
    refund_at = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users_rel = db.relationship('UserRepository')
    items = db.Column(MutableList.as_mutable(db.PickleType), nullable=False)

    def __init__(self, user_id: int, amount: float, payment_at: float, total_quantity: int,
                 items: list[dict], state: str, id: int | None = None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.payment_at = payment_at
        self.items = items
        self.total_quantity = total_quantity
        self.state = state

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
                "user_id": self.user_id,
                "amount": self.amount,
                "total_quantity": self.total_quantity,
                "items": self.items,
                "payment_at": self.payment_at,
                "state": self.state}
