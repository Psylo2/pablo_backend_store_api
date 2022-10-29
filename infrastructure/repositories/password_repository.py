from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class PasswordRepository(db.Model, RepositoryInterface):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    current_password = db.Column(db.LargeBinary, nullable=False)
    last_change = db.Column(db.Float, nullable=True)
    password_last_1 = db.Column(db.LargeBinary, nullable=True)
    password_last_2 = db.Column(db.LargeBinary, nullable=True)
    password_last_3 = db.Column(db.LargeBinary, nullable=True)
    password_last_4 = db.Column(db.LargeBinary, nullable=True)
    password_last_5 = db.Column(db.LargeBinary, nullable=True)
    password_last_6 = db.Column(db.LargeBinary, nullable=True)
    password_last_7 = db.Column(db.LargeBinary, nullable=True)
    password_last_8 = db.Column(db.LargeBinary, nullable=True)
    password_last_9 = db.Column(db.LargeBinary, nullable=True)
    password_last_10 = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, id: int | None, username: str, current_password: bytes, last_change: float = None):
        self.id = id
        self.username = username
        self.current_password = current_password
        self.last_change = last_change

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
                "username": self.username,
                "current_password": self.current_password,
                "password_last_1": self.password_last_1,
                "password_last_2": self.password_last_2,
                "password_last_3": self.password_last_3,
                "password_last_4": self.password_last_4,
                "password_last_5": self.password_last_5,
                "password_last_6": self.password_last_6,
                "password_last_7": self.password_last_7,
                "password_last_8": self.password_last_8,
                "password_last_9": self.password_last_9,
                "password_last_10": self.password_last_10,
                "last_change": self.last_change}
