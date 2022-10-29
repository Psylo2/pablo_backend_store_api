from infrastructure.repositories.subscriber_repository import SubscriberRepository
from infrastructure.interfaces.repositories.queries.subscriber_queries_interface import SubscriberQueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class SubscriberQueries(SubscriberQueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> SubscriberRepository:
        subscriber = SubscriberRepository(**data)
        subscriber.add_to_repository()
        return subscriber

    def remove(self, entity: SubscriberRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> SubscriberRepository:
        return SubscriberRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[SubscriberRepository]:
        return SubscriberRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[SubscriberRepository]:
        return SubscriberRepository.query.filter_by(**{key: value}
                                                    ).order_by(
            self.repository_services.db.desc(SubscriberRepository.id)).all()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def count_confirms(self, id: int) -> int:
        tot = SubscriberRepository.query.with_entities(
            self.repository_services.func.count(SubscriberRepository.confirmed)).filter_by(id=id).all()
        return 0 if tot[0][0] is None else tot[0][0]

    def update(self, entity: SubscriberRepository) -> None:
        entity.update_repository()
