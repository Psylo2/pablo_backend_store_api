from abc import ABC, abstractmethod
from typing import TypeVar

from infrastructure.interfaces.repositories.queries.base_queries_interface import BaseQueriesInterface

T = TypeVar("T")


class UserQueriesInterface(BaseQueriesInterface, ABC):

    @abstractmethod
    def most_recent_confirmation(self) -> int:
        ...

    @abstractmethod
    def encrypt(self, str_field: str) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, str_field: str, byte_field: bytes) -> bool:
        ...
