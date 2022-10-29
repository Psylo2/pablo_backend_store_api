from abc import ABC, abstractmethod
from typing import TypeVar

T_PAYMENT = TypeVar("T_PAYMENT")

class PaymentsApiInterface(ABC):

    @abstractmethod
    def charge_payment(self, token: str, payment: T_PAYMENT, email: str) -> dict:
        ...

    @abstractmethod
    def refund_payment(self, payment: T_PAYMENT) -> dict:
        ...
