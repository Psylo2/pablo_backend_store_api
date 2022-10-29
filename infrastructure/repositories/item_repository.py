from infrastructure.repositories.repository_manager import repository
from infrastructure.interfaces.repositories.repository_interface import RepositoryInterface

db = repository.db


class ItemRepository(db.Model, RepositoryInterface):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    on_sale = db.Column(db.Boolean(False), nullable=False)
    on_stock = db.Column(db.Boolean(True), nullable=False)
    sold = db.Column(db.Boolean(False), nullable=False)
    engine_hs_power = db.Column(db.Integer, nullable=False, default=0)
    original_price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False, default=0)
    file_path = db.Column(db.String(200), nullable=False)
    new_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.Float)
    last_modified = db.Column(db.Float)

    def __init__(self,
                 title: str, manufacturer: str, engine_hs_power: int, original_price: float,
                 on_sale: bool | str, discount: int, new_price: float, on_stock: bool | str, file_path: str,
                 created_at: float, last_modified: float, sold: bool = False, id: int | None = None,
                 user_id: int | None = None):
        self.id = id
        self.title = title
        self.manufacturer = manufacturer
        self.engine_hs_power = engine_hs_power
        self.original_price = original_price
        self.on_sale = True if on_sale == 'true' else False
        self.discount = discount
        self.new_price = new_price
        self.on_stock = True if on_stock == 'true' else False
        self.file_path = file_path
        self.sold = sold
        self.created_at = created_at
        self.last_modified = last_modified
        self.user_id = user_id

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
                "title": self.title,
                "manufacturer": self.manufacturer,
                "engine_hs_power": self.engine_hs_power,
                "original_price": self.original_price,
                "on_sale": self.on_sale,
                "discount": self.discount,
                "new_price": self.new_price,
                "on_stock": self.on_stock,
                "file_path": self.file_path,
                "user_id": self.user_id,
                "sold": self.sold,
                "last_modified": self.last_modified}
