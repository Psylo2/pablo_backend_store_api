from infrastructure.repositories.confirmation_repository import ConfirmationRepository
from infrastructure.interfaces.repositories.queries.confirmation_queries_interface import ConfirmationQueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class ConfirmationQueries(ConfirmationQueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> ConfirmationRepository:
        confirmation = ConfirmationRepository(**data)
        confirmation.add_to_repository()
        return confirmation

    def remove(self, entity: ConfirmationRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> ConfirmationRepository:
        return ConfirmationRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[ConfirmationRepository]:
        return ConfirmationRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[ConfirmationRepository]:
        return ConfirmationRepository.query.filter_by(**{key: value}
                                                      ).order_by(
            self.repository_services.db.desc(ConfirmationRepository.id)).all()

    def update(self, entity: ConfirmationRepository) -> None:
        entity.update_repository()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def find_last_by_user_id(self, id: int) -> ConfirmationRepository:
        return ConfirmationRepository.filter_by(id=id).order_by(
            self.repository_services.db.desc(ConfirmationRepository.expired_at)).first()

    def count_confirms(self, id: int) -> int:
        tot = ConfirmationRepository.query.with_entities(
            self.repository_services.func.count(ConfirmationRepository.confirmed)).filter_by(id=id).all()
        return 0 if tot[0][0] is None else tot[0][0]


