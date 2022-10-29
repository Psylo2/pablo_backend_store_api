from abc import ABC, abstractmethod
from typing import TypeVar

from infrastructure.interfaces.repositories.queries.base_queries_interface import BaseQueriesInterface

T = TypeVar("T")


class ConfirmationQueriesInterface(BaseQueriesInterface, ABC):

    @abstractmethod
    def find_last_by_user_id(self, id: int) -> T:
        ...

    @abstractmethod
    def count_confirms(self, id: int) -> int:
        ...
