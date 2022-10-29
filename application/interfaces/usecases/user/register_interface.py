from abc import ABC, abstractmethod

class RegisterInterface(ABC):

    @abstractmethod
    def user_register(self, user_data: dict) -> tuple:
        ...
