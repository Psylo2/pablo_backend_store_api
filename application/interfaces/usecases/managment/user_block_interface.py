from abc import ABC, abstractmethod

class UserBlockInterface(ABC):

    @abstractmethod
    def block_user(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def unblock_user(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        ...
