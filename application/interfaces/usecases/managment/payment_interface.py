from abc import ABC, abstractmethod


class PaymentInterface(ABC):

    @abstractmethod
    def payment(self, identity: any, data: dict) -> tuple:
        ...

    @abstractmethod
    def full_refund(self, identity: any, data: dict) -> tuple:
        ...

    @abstractmethod
    def get_user_payments(self, identity: any) -> tuple[dict, int]:
        ...

    @abstractmethod
    def all_payments(self, jwt_data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def paid_payments(self, jwt_data: dict) -> tuple:
        ...

    @abstractmethod
    def pending_payments(self, jwt_data: dict) -> tuple:
        ...

    @abstractmethod
    def fail_payments(self, jwt_data: dict) -> tuple:
        ...

    @abstractmethod
    def get_user_refund(self, identity: any) -> tuple:
        ...
