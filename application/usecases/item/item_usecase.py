import json
from urllib.parse import unquote
from logging import Logger
from typing import TypeVar

from domain.entities.pagination_entity import Pagination
from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.usecases.item.decorators.function_decorators import items_display
from application.interfaces.usecases.item.item_interface import ItemInterface, PaginatedItemsDict, Platform, Order, SortByDict
from application.exceptions import PaginationError

from infrastructure.interfaces.repositories.queries_interface import QueriesInterface, PaginationQueriesInterface

T_ITEM = TypeVar("T_ITEM")

class ItemUseCase(ItemInterface):
    def __init__(self,
                 repository_queries: QueriesInterface | PaginationQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def get_items(self, data: dict[str, any]) -> tuple[PaginatedItemsDict, int]:
        platform, sort_by, order = self._extract_fields(data=data)
        repository_query = self.repository_queries.fetch_all_by_multi_fields \
            if sort_by else self.repository_queries.fetch_all_order_by

        items = repository_query(order=order, sort_by=sort_by)
        items_list = self._display(items=items)
        paginated_items_dict = self._paginate_item_list(platform=platform, items_list=items_list)

        return paginated_items_dict, 200

    def get_items_manufacturer(self, data: dict) -> tuple[dict[str, list], int]:
        items = self.repository_queries.fetch_all_sorted_by(key='manufacturer', value=data['manufacturer'])
        items_list = self._display(items=items)
        return {"items": items_list}, 200

    @items_display
    def _display(self, items: list[T_ITEM]) -> list[T_ITEM]:
        return items

    @staticmethod
    def _extract_fields(data: dict[str, any]) -> tuple[Platform, SortByDict, Order]:
        platform = data.get('platform')
        sort_by = data.get('sort_by')
        order = data.get('order')

        if platform not in Platform.__args__:
            raise PaginationError(f"Invalid value for platform, chose from {Platform.__args__}")

        if sort_by:
            sort_by = unquote(sort_by)
            if not sort_by.startswith("{") and sort_by.endswith("}"):
                raise PaginationError(f"Invalid value for sort_by")

            sort_by = json.loads(sort_by)
            for key, value in sort_by.items():
                if not isinstance(value, (int, str, bool)):
                    raise PaginationError(f"Invalid value for sort_by ({key}: {value})")

                if key not in {"on_stock", "price", "manufacturer", "engine_hs_power", "on_sale"}:
                    raise PaginationError(f"Invalid key for sort_by ({key})")

        if order not in Order.__args__:
            raise PaginationError(f"Invalid value for order, chose from {Order.__args__}")

        return platform, sort_by, order

    @staticmethod
    def _paginate_item_list(platform: Platform, items_list: list[dict]) -> PaginatedItemsDict:
        chunk_per_page: int = Pagination[platform.upper()].value
        page = 1
        paginated_items = {}
        for index in range(0, len(items_list), chunk_per_page):
            paginated_items.update(
                {page: items_list[index:index + chunk_per_page]}
            )
            page += 1

        return paginated_items
