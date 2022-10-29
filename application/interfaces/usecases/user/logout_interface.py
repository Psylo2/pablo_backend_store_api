from abc import ABC, abstractmethod

class LogoutInterface(ABC):

    @abstractmethod
    def user_logout(self, data: dict) -> tuple:
        ...
