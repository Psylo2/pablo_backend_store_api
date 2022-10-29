from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class UserRepository(db.Model, RepositoryInterface):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    blocked = db.Column(db.Boolean(False), nullable=False)
    create_at = db.Column(db.Float, nullable=True)
    last_login = db.Column(db.Float, nullable=True)
    confirmation = db.relationship("ConfirmationRepository", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, name: str, email: str, password: str, blocked: bool = None, id: int = None,
                 create_at: float = None, last_login: float = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.create_at = create_at
        self.last_login = last_login
        self.blocked = blocked

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
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "blocked": self.blocked,
                "create_at": self.create_at,
                "last_login": self.last_login}
