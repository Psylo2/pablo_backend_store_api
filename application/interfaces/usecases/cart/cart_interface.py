from abc import ABC, abstractmethod

class CartInterface(ABC):

    @abstractmethod
    def show_cart(self, identity: any) -> tuple:
        ...

    @abstractmethod
    def remove_cart(self, identity: any) -> tuple:
        ...

    @abstractmethod
    def add_item(self, data: dict) -> tuple:
        ...

    @abstractmethod
    def remove_item(self, data: dict) -> tuple:
        ...

    @abstractmethod
    def carts_list(self, jwt_data: dict) -> tuple:
        ...
