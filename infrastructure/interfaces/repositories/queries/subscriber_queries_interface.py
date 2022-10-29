from abc import ABC, abstractmethod
from typing import TypeVar

from infrastructure.interfaces.repositories.queries.base_queries_interface import BaseQueriesInterface

T = TypeVar("T")


class SubscriberQueriesInterface(BaseQueriesInterface, ABC):

    @abstractmethod
    def count_confirms(self, id: int) -> int:
        ...
