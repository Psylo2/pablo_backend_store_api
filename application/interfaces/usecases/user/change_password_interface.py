from abc import ABC, abstractmethod


class ChangePasswordInterface(ABC):

    @abstractmethod
    def send_confirmation_email(self, data: dict) -> tuple:
        ...

    @abstractmethod
    def confirm_email(self, data: dict) -> tuple:
        ...

    @abstractmethod
    def change_password(self, data: dict) -> tuple:
        ...
