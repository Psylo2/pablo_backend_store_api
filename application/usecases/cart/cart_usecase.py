from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.usecases.cart.cart_interface import CartInterface
from application.exceptions import CartError, ItemError, AdminError

from infrastructure.interfaces.repositories.queries.cart_queries_interface import CartQueriesInterface
from infrastructure.interfaces.repositories.queries.item_queries_interface import ItemQueriesInterface

T_ITEM = TypeVar("T_ITEM")
T_CART = TypeVar("T_CART")


class CartUseCase(CartInterface):
    def __init__(self,
                 repository_queries: CartQueriesInterface,
                 item_repository_queries: ItemQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.item_repository_queries = item_repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def show_cart(self, identity: any) -> tuple:
        cart = self.repository_queries.find_by(key='user_id', value=identity)
        if not cart:
            return self._empty_cart_payload(), 200
        return self._show_cart_payload(cart=cart), 200

    def remove_cart(self, identity: any) -> tuple:
        cart = self.repository_queries.find_by(key='user_id', value=identity)
        self.repository_queries.remove(entity=cart)
        return self._empty_cart_payload(), 200

    def add_item(self, data: dict) -> tuple:
        cart = self.repository_queries.find_by(key="user_id", value=data["user_id"])
        item = self.item_repository_queries.find_by(key="id", value=data["item_id"])

        if not item:
            raise ItemError(self.language_manager.get("item_not_found"))
        if item.sold:
            raise ItemError(self.language_manager.get("item_not_available"))

        cart = self._create_cart(data=data) if not cart else cart
        self._check_item_in_cart(item=item, cart=cart)
        self._append_item_to_cart(item=item, cart=cart)

        return {"message": self.language_manager.get("item_added_to_cart")}, 200

    def remove_item(self, data: dict) -> tuple:
        cart = self.repository_queries.find_by(key="user_id", value=data["user_id"])
        item = self.item_repository_queries.find_by(key="id", value=data["item_id"])

        if not item:
            raise ItemError(self.language_manager.get("item_not_found"))
        if item.to_dict() not in cart.items:
            raise CartError(self.language_manager.get("item_not_in_cart"))

        self._remove_item_to_cart(item=item, cart=cart)
        return {"message": self.language_manager.get("item_removed")}, 200

    def carts_list(self, jwt_data: dict) -> tuple:
        if not jwt_data['is_admin']:
            raise AdminError(self.language_manager.get("admin_privilege"))

        carts_list = self.repository_queries.fetch_all()
        return {"carts": carts_list}, 200

    @staticmethod
    def _empty_cart_payload() -> dict[str, list | int]:
        return {
            'items': [],
            'quantity': 0,
            'amount': 0
        }

    def _remove_item_to_cart(self, item: T_ITEM, cart: T_CART) -> None:
        cart.items.remove(item.to_dict())
        self.repository_queries.update(entity=cart)

    def _show_cart_payload(self, cart: T_CART) -> dict:
        total_amount = 0
        total_quantity = 0
        item_titles: dict[str, dict] = {}

        for item_dict in cart.items:
            item = self.item_repository_queries.find_by(key="id", value=item_dict['id'])
            if item.sold:
                continue

            self._enrich_item_display(item=item, item_titles=item_titles)
            total_quantity += 1
            total_amount += item.new_price

        items = [v for k, v in item_titles.items()]
        return self._cart_payload(items=items, total_amount=total_amount)

    def _enrich_item_display(self, item: T_ITEM, item_titles: dict[str, dict]) -> None:
        updated_item_dict = item.to_dict()
        item_by_title = item_titles.get(item.title)

        if not item_by_title:
            updated_item_dict['ids'] = [updated_item_dict.pop('id')]
            updated_item_dict['quantity'] = 1
            item_titles.update({item.title: updated_item_dict})
            return

        ids = item_titles[item.title]['ids']
        if item.id in ids:
            raise CartError(self.language_manager.get("item_already_in_cart"))
        item_titles[item.title]['ids'].append(updated_item_dict.pop('id'))
        item_titles[item.title]['quantity'] += 1

    @staticmethod
    def _cart_payload(items: list[dict], total_amount: int) -> dict:
        quantity_list = [item['quantity'] for item in items]

        return {'items': items,
                'quantity': sum(quantity_list),
                'amount': total_amount}

    def _check_item_in_cart(self, item: T_ITEM, cart: T_CART) -> None:
        exists_items_id = []
        for item_dict in cart.items:
            item_id = item_dict['id']
            if item_id in exists_items_id:
                continue

            if item_id == item.id:
                all_title_items = self.item_repository_queries.fetch_all_sorted_by(key="title", value=item.title)
                same_items = [item for item in all_title_items if not item.sold]
                if not same_items:
                    raise CartError(self.language_manager.get("item_already_in_cart"))

                for same_item in same_items:
                    if not same_item.sold and same_item.id not in exists_items_id:
                        item_dict['id'] = same_item.id
                        break

            exists_items_id.append(item_id)

    def _append_item_to_cart(self, item: T_ITEM, cart: T_CART) -> None:
        cart.items.append(item.to_dict())
        self.repository_queries.update(entity=cart)

    def _create_cart(self, data: dict) -> T_CART:
        data.pop('item_id')
        timestamp = self.repository_queries.insert_timestamp()
        data.update({"created_at": timestamp, "last_modified": timestamp, "items": []})
        cart = self.repository_queries.save(data=data)
        return cart
