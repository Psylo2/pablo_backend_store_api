from abc import ABC
from typing import TypeVar

from infrastructure.interfaces.repositories.queries.base_queries_interface import BaseQueriesInterface

T = TypeVar("T")


class PaymentQueriesInterface(BaseQueriesInterface, ABC):
    ...
