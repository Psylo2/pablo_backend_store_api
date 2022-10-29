from abc import ABC, abstractmethod

class ChangePasswordInterface(ABC):

    @abstractmethod
    def change_password(self, data: dict) -> tuple:
        ...
