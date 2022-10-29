from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")

class QueriesInterface(ABC):

    @abstractmethod
    def save(self, data: dict) -> T:
        ...

    @abstractmethod
    def remove(self, entity: T) -> None:
        ...

    @abstractmethod
    def find_by(self, key: str, value: any) -> T:
        ...

    @abstractmethod
    def fetch_all(self) -> list[T]:
        ...

    @abstractmethod
    def fetch_all_sorted_by(self, key: str, value: any) -> list[T]:
        ...

    @abstractmethod
    def update(self, entity: T) -> None:
        ...

    def insert_timestamp(self) -> float:
        ...

    def convert_timestamp(self, timestamp: float) -> str:
        ...


class PaginationQueriesInterface(ABC):
    @abstractmethod
    def fetch_all_order_by(self, order: str, **kwargs) -> list[T]:
        ...

    @abstractmethod
    def fetch_all_by_multi_fields(self, order: str, sort_by: dict[str, int | str | bool]) -> list[T]:
        ...
