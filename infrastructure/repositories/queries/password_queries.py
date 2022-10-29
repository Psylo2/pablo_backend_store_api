from infrastructure.repositories.password_repository import PasswordRepository
from infrastructure.interfaces.repositories.queries_interface import QueriesInterface
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface


class PasswordQueries(QueriesInterface):
    def __init__(self, repository_services: RepositoryManagerInterface):
        self.repository_services = repository_services

    def save(self, data: dict) -> PasswordRepository:
        password = PasswordRepository(**data)
        password.add_to_repository()
        return password

    def remove(self, entity: PasswordRepository) -> None:
        entity.remove_from_repository()

    def find_by(self, key: str, value: any) -> PasswordRepository:
        return PasswordRepository.query.filter_by(**{key: value}).first()

    def fetch_all(self) -> list[PasswordRepository]:
        return PasswordRepository.query.all()

    def fetch_all_sorted_by(self, key: str, value: any) -> list[PasswordRepository]:
        return PasswordRepository.query.filter_by(**{key: value}
                                              ).order_by(self.repository_services.db.desc(PasswordRepository.id)).all()

    def update(self, entity: PasswordRepository) -> None:
        entity.update_repository()

    def insert_timestamp(self) -> float:
        return self.repository_services.insert_timestamp()

    def convert_timestamp(self, timestamp: float) -> str:
        return self.repository_services.convert_timestamp(timestamp=timestamp)

    def encrypt(self, str_field: str) -> bytes:
        return self.repository_services.encrypt(str_field=str_field)

    def decrypt(self, str_field: str, byte_field: bytes) -> bool:
        return self.repository_services.decrypt(str_field=str_field, byte_field=byte_field)
