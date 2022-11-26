import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.usecases.item.decorators.function_decorators import items_display, sold_items_display
from application.interfaces.usecases.managment.item_inventory_interface import ItemInventoryInterface
from application.exceptions import ItemError, AdminError

from infrastructure.interfaces.repositories.queries.item_queries_interface import ItemQueriesInterface

T_ITEM = TypeVar("T_ITEM")


class ItemInventoryUseCase(ItemInventoryInterface):
    accepted_image_mimetype: set[str] = {'image/png', 'image/jpeg', 'image/pjpeg'}
    engine_hs_power_set = {60, 90, 130, 155, 230, 300}
    manufacturers_set = {"SeaDoo", "Spark", "FISHPRO"}
    item_boolean_fields = ['on_stock', 'on_sale']
    boolean_mapper = {"true": True, "false": False}

    def __init__(self,
                 repository_queries: ItemQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def show_item(self, jwt_data: dict, data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)

        item_id = data.pop('id')
        item = self.repository_queries.find_by(key="id", value=item_id)
        if not item:
            raise ItemError(self.language_manager.get("item_not_found"))
        return item.to_dict(), 200

    def create_item(self, jwt_data: dict, data: dict, file: FileStorage | None) -> tuple[dict, int]:
        self._check_admin_privilege(jwt_data=jwt_data)

        title = data['title']
        self._validate_title(title=title)
        self._validate_file(file=file)

        file_path = self._generate_file_path(file=file)
        self.logger.info(f"File Path:   {file_path}")
        self._validate_file_path(file_path=file_path)

        return self._create_item(data=data, file=file, file_path=file_path)

    def update_item(self, jwt_data: dict, data: dict, file: FileStorage | None) -> tuple[dict, int]:
        self._check_admin_privilege(jwt_data=jwt_data)

        title = data.pop('title')
        data['file_path'] = file
        self._validate_boolean_fields(data=data, fields=self.item_boolean_fields)

        data = {key: value for key, value in data.items() if value is not None}
        if not data:
            return {}, 200

        items: list[T_ITEM] = self.repository_queries.fetch_all_sorted_by(key="title", value=title)
        if not items:
            return {"message": self.language_manager.get("item_not_found")}, 401

        return self._update_item(data=data, items=items)

    def remove_item(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        self._check_admin_privilege(jwt_data=jwt_data)

        title = data['title']
        if not self.field_validation_manager.item_name_regex(title):
            raise ItemError(self.language_manager.get("invalid_string"))

        items = self.repository_queries.fetch_all_sorted_by(key="title", value=title)
        if not items:
            raise ItemError(self.language_manager.get("item_not_found"))

        filename = items[0].file_path
        [self.repository_queries.remove(item) for item in items if not item.sold]

        items_sold = self.repository_queries.fetch_all_sorted_by(key="title", value=title)
        items = [item for item in items_sold if not item.sold]
        if not items:
            if os.path.exists(filename):
                os.remove(filename)

        return {}, 200

    def items_list(self, jwt_data: dict) -> tuple[dict, int]:
        self._check_admin_privilege(jwt_data=jwt_data)
        items_list = self.repository_queries.fetch_all()
        items = self._display(items=items_list)
        return {"items": items}, 200

    def sold_items_list(self, jwt_data: dict) -> tuple[dict, int]:
        self._check_admin_privilege(jwt_data=jwt_data)
        items_list = self.repository_queries.fetch_all()
        items = self._display_only_sold(items=items_list)
        return {"items": items}, 200

    @items_display
    def _display(self, items: list[T_ITEM]) -> list[T_ITEM]:
        return items

    @sold_items_display
    def _display_only_sold(self, items: list[T_ITEM]) -> list[T_ITEM]:
        return items

    @staticmethod
    def _calculate_new_price(original_price: int, discount: int) -> int:
        return int(original_price - (0.01 * discount) * original_price)

    def _create_item(self, data: dict, file: FileStorage, file_path: str) -> tuple[dict, int]:
        data['created_at'] = self.repository_queries.insert_timestamp()
        data['last_modified'] = self.repository_queries.insert_timestamp()
        data['engine_hs_power'] = abs(data['engine_hs_power'])

        original_price = abs(data['original_price'])
        discount = abs(data['discount']) if data['on_sale'] else 0
        data['original_price'] = original_price
        data['discount'] = discount
        data['new_price'] = self._calculate_new_price(original_price=original_price, discount=discount)

        if not self.field_validation_manager.item_name_regex(data['manufacturer']):
            raise ItemError(self.language_manager.get("invalid_string"))
        quantity = abs(data.pop('quantity', 0))
        item = None

        try:
            file.save(dst=file_path)
            data['file_path'] = file_path.replace(os.environ.get('UPLOAD_FOLDER'), '/img/')

            for _ in range(quantity):
                item = self.repository_queries.save(data=data)
            self.logger.info(f"Item created: {item.to_dict()}")

            return {}, 200

        except Exception as err:
            if item:
                self.repository_queries.remove(entity=item)
            os.remove(file_path)
            return {"message": self.language_manager.get("error_occurred"),
                    "details": str(err)}, 500

    @staticmethod
    def _generate_file_path(file: FileStorage) -> str:
        secured_file_name = secure_filename(filename=file.filename)
        file_path = os.environ.get('UPLOAD_FOLDER', '') + secured_file_name
        return file_path

    def _is_valid_file_mimetype(self, file: FileStorage) -> bool:
        return file.mimetype not in self.accepted_image_mimetype

    def _check_admin_privilege(self, jwt_data: dict) -> None:
        if not jwt_data['is_admin']:
            raise AdminError(self.language_manager.get("admin_privilege"))

    def _validate_title(self, title: str) -> None:
        is_item_name_exists = self.repository_queries.find_by(key="title", value=title)
        if is_item_name_exists:
            raise ItemError(self.language_manager.get("item_name_exists"))

        if not self.field_validation_manager.item_name_regex(title):
            raise ItemError(self.language_manager.get("invalid_string"))

    def _validate_file(self, file: FileStorage | None) -> None:
        if not file:
            raise ItemError(self.language_manager.get("file_not_found"))

        if self._is_valid_file_mimetype(file=file):
            message = self.language_manager.get("invalid_file_mimetype").format(self.accepted_image_mimetype)
            raise ItemError(message)

    def _validate_file_path(self, file_path: str) -> None:
        is_file_exist = os.path.exists(path=file_path)
        if is_file_exist:
            raise ItemError(self.language_manager.get("file_name_exists"))

    def _update_item(self, data: dict, items: list[T_ITEM]) -> tuple[dict, int]:
        old_filename = items[0].file_path
        updated_data = self._enrich_update_data(data=data, items=items)

        for item in items:
            if item.sold:
                continue

            [setattr(item, key, value) for key, value in updated_data.items()]
            self.repository_queries.update(entity=item)

        updated_filename = items[0].file_path
        self._update_file(old_filename=old_filename, updated_filename=updated_filename)

        return {}, 200

    def _enrich_update_data(self, data: dict, items: list[T_ITEM]) -> dict:
        current_item_data = items[0]

        item_fields_mapper = {
            "manufacturer": self._update_manufacturer,
            "engine_hs_power": self._update_engine_hs_power,
            "discount": self._update_discount,
            "on_sale": self._update_on_sale,
            "on_stock": self._update_on_stock,
            "original_price": self._update_original_price,
            "file_path": self._update_file_path
        }

        [item_fields_mapper[key](new_value=value, item=current_item_data) for key, value in data.items()]
        self._update_new_price(item=current_item_data)
        current_item_data.last_modified = self.repository_queries.insert_timestamp()
        updated_data = current_item_data.to_dict()
        updated_data.pop('id')
        return updated_data

    def _update_manufacturer(self, new_value: str, item: T_ITEM) -> None:
        if not self.field_validation_manager.item_name_regex(new_value) or \
                new_value not in self.manufacturers_set:
            raise ItemError(self.language_manager.get("invalid_string"))

        item.manufacturer = new_value

    def _update_engine_hs_power(self, new_value: int, item: T_ITEM) -> None:
        if new_value not in self.engine_hs_power_set:
            raise ItemError(self.language_manager.get("invalid_string"))

        item.engine_hs_power = abs(new_value)

    def _update_on_sale(self, new_value: str, item: T_ITEM) -> None:
        item.on_sale = self._enrich_boolean_field(value=new_value)

    def _update_on_stock(self, new_value: str, item: T_ITEM) -> None:
        item.on_stock = self._enrich_boolean_field(value=new_value)

    def _update_discount(self, new_value: int, item: T_ITEM) -> None:
        if new_value < 0:
            raise ItemError(self.language_manager.get("invalid_string"))

        item.discount = abs(new_value)

    def _update_original_price(self, new_value: int, item: T_ITEM) -> None:
        if new_value < 0:
            raise ItemError(self.language_manager.get("invalid_string"))

        item.original_price = abs(new_value)

    def _update_new_price(self, item: T_ITEM) -> None:
        if item.on_sale:
            item.discount = 0

        item.new_price = self._calculate_new_price(original_price=item.original_price, discount=item.discount)

    def _update_file_path(self, new_value: FileStorage, item: T_ITEM) -> None:
        self._validate_file(file=new_value)
        file_path = self._generate_file_path(file=new_value)
        self._validate_file_path(file_path=file_path)

        new_value.save(dst=file_path)
        item.file_path = file_path.replace(os.environ.get('UPLOAD_FOLDER', ''), '/img/')

    @staticmethod
    def _update_file(old_filename: str, updated_filename: str) -> None:
        if old_filename == updated_filename:
            return

        old_file_path = os.environ.get('UPLOAD_FOLDER', '') + old_filename.replace('/img/', '')
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

    def _enrich_boolean_field(self, value: str) -> bool:
        value = self.boolean_mapper.get(value)
        if value is None:
            raise ItemError(self.language_manager.get("invalid_string"))

        return value

    @staticmethod
    def _validate_boolean_fields(data: dict, fields: list[str]) -> None:
        for field in fields:
            if data.get(field) == '--feature':
                data[field] = None
