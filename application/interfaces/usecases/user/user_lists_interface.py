from abc import ABC, abstractmethod

class UserListsInterface(ABC):

    @abstractmethod
    def allowed_users_list(self, jwt_data: dict) -> tuple:
        ...

    @abstractmethod
    def blocked_users_list(self, jwt_data: dict) -> tuple:
        ...

    @abstractmethod
    def all_users_list(self, jwt_data: dict) -> tuple:
        ...
