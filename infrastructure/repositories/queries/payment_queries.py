from infrastructure.repositories.paymanet_repository import PaymentRepository
from infrastructure.interfaces.repositories.queries.payment_queries_interface import PaymentQueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class PaymentQueries(PaymentQueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> PaymentRepository:
        payment = PaymentRepository(**data)
        payment.add_to_repository()
        return payment

    def remove(self, entity: PaymentRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> PaymentRepository:
        return PaymentRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[PaymentRepository]:
        return PaymentRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[PaymentRepository]:
        return PaymentRepository.query.filter_by(**{key: value}
                                                 ).order_by(
            self.repository_services.db.desc(PaymentRepository.id)).all()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def update(self, entity: PaymentRepository) -> None:
        entity.update_repository()
