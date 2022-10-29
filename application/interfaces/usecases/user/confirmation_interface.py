from abc import ABC, abstractmethod

class ConfirmationInterface(ABC):

    @abstractmethod
    def send_email_confirmation(self, user_data: dict) -> None:
        ...

    @abstractmethod
    def confirm(self, confirmation_data: dict) -> tuple:
        ...

    @abstractmethod
    def is_user_confirmed(self, user_id: int) -> bool:
        ...
