from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage


class ItemInventoryInterface(ABC):

    @abstractmethod
    def show_item(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def create_item(self, jwt_data: dict, data: dict, file: FileStorage | None) -> tuple[dict, int]:
        ...

    @abstractmethod
    def update_item(self, jwt_data: dict, data: dict, file: FileStorage | None) -> tuple[dict, int]:
        ...

    @abstractmethod
    def remove_item(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def items_list(self, jwt_data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def sold_items_list(self, jwt_data: dict) -> tuple[dict, int]:
        ...
