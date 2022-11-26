from abc import ABC, abstractmethod
from typing import Literal

PaginatedItemsDict = dict[int, list[dict]]
Platform = Literal["pc", "mobile"]
SortByDict = dict[str, str | int | bool]
Order = Literal["asc", "desc"]


class ItemInterface(ABC):

    @abstractmethod
    def get_items(self, data: dict[str, any]) -> tuple[PaginatedItemsDict, int]:
        ...

    @abstractmethod
    def get_items_manufacturer(self, data: dict) -> dict[list[str]]:
        ...

    @abstractmethod
    def get_item(self, data: dict) -> tuple[dict[str, dict], int]:
        ...
