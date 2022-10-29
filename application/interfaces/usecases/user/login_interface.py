from abc import ABC, abstractmethod

class LoginInterface(ABC):

    @abstractmethod
    def user_login(self, user_data: dict) -> tuple:
        ...
