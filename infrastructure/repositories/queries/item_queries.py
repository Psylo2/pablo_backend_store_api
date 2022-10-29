from infrastructure.repositories.item_repository import ItemRepository
from infrastructure.interfaces.repositories.queries_interface import QueriesInterface, PaginationQueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class ItemQueries(QueriesInterface, PaginationQueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> ItemRepository:
        item = ItemRepository(**data)
        item.add_to_repository()
        return item

    def remove(self, entity: ItemRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> ItemRepository:
        return ItemRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[ItemRepository]:
        return ItemRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[ItemRepository]:
        return ItemRepository.query.filter_by(**{key: value}
                                              ).order_by(self.repository_services.db.desc(ItemRepository.id)).all()

    def fetch_all_order_by(self, order: str, **kwargs) -> list[ItemRepository]:
        _order = self.repository_services.db.asc if order == "asc" else self.repository_services.db.desc
        return ItemRepository.query.filter_by(**{"user_id": None}).order_by(_order(ItemRepository.id)).all()

    def fetch_all_by_multi_fields(self, order: str, sort_by: dict[str, int | str | bool]) -> list[ItemRepository]:
        filter_many = []
        _and = self.repository_services.db.and_
        _order = self.repository_services.db.asc if order == "asc" else self.repository_services.db.desc
        filter_many.append(ItemRepository.user_id is None)

        if sort_by.get('on_stock'):
            filter_many.append(ItemRepository.on_stock == sort_by['on_stock'])

        if sort_by.get('price'):
            min_price, max_price = sort_by['price'].split('_')
            filter_many.append(ItemRepository.original_price >= min_price)
            filter_many.append(ItemRepository.original_price <= max_price)

        if sort_by.get('manufacturer'):
            filter_many.append(ItemRepository.manufacturer == sort_by['manufacturer'])

        if sort_by.get('engine_hs_power'):
            filter_many.append(ItemRepository.engine_hs_power == sort_by['engine_hs_power'])

        if sort_by.get('on_sale'):
            filter_many.append(ItemRepository.on_sale == sort_by['on_sale'])

        return ItemRepository.query.filter(_and(*filter_many)).order_by(_order(ItemRepository.id)).all()


    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def update(self, entity: ItemRepository) -> None:
        entity.update_repository()
