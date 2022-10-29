from infrastructure.repositories.cart_repository import CartRepository
from infrastructure.interfaces.repositories.queries_interface import QueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class CartQueries(QueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> CartRepository:
        cart = CartRepository(**data)
        cart.add_to_repository()
        return cart

    def remove(self, entity: CartRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> CartRepository:
        return CartRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[CartRepository]:
        return CartRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[CartRepository]:
        return CartRepository.query.filter_by(**{key: value}
                                              ).order_by(self.repository_services.db.desc(CartRepository.id)).all()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def update(self, entity: CartRepository) -> None:
        entity.update_repository()
