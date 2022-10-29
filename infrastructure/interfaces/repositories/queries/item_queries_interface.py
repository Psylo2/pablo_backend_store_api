from abc import ABC
from typing import TypeVar

from infrastructure.interfaces.repositories.queries.base_queries_interface import (BaseQueriesInterface,
                                                                                   PaginationQueriesInterface)

T = TypeVar("T")


class ItemQueriesInterface(BaseQueriesInterface, PaginationQueriesInterface, ABC):
    ...
