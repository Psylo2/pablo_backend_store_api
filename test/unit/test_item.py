from unittest import TestCase
from pydantic.error_wrappers import ValidationError

from domain.entities.item_entity import ItemEntity

class TestItemEntity(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_entity = MockEntity()

    def test_entity_valid_item_all_fields(self) -> None:
        item = ItemEntity(**self.mock_entity.mock_valid_item_all_fields())
        self.assertTrue(expr=item, msg="Valid item")

    def test_entity_valid_item_required_fields_only(self) -> None:
        item = ItemEntity(**self.mock_entity.mock_valid_item_required_fields_only())
        self.assertTrue(expr=item, msg="Valid item")

    def test_entity_invalid_item_id(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_id())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid id")

    def test_entity_invalid_item_name(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_name())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid name")
        
    def test_entity_invalid_item_price(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_price())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid price")

    def test_entity_invalid_item_user_id(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_user_id())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid user_id")

    def test_entity_invalid_item_create_at(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_create_at())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid created_at")

    def test_entity_invalid_item_last_modified(self) -> None:
        try:
            item = ItemEntity(**self.mock_entity.mock_item_with_invalid_create_at())
        except ValidationError:
            item = None
        self.assertFalse(expr=item, msg="Invalid last_modified")


class MockEntity:

    @staticmethod
    def mock_valid_item_all_fields() -> dict:
        return {"id": 12,
                "name": "item",
                "price": 10.02,
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_valid_item_required_fields_only() -> dict:
        return {"name": "item",
                "price": 10.02}

    @staticmethod
    def mock_item_with_invalid_id() -> dict:
        return {"id": "a",
                "name": "item",
                "price": 10.02,
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_item_with_invalid_name() -> dict:
        return {"id": "a",
                "name": 213,
                "price": 10.02,
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}
    
    @staticmethod
    def mock_item_with_invalid_price() -> dict:
        return {"id": 12,
                "name": 213,
                "price": "aw",
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_item_with_invalid_user_id() -> dict:
        return {"id": 12,
                "name": 213,
                "price": 10.02,
                "user_id": "e",
                "create_at": 11.1,
                "last_modified": 123.12}
    
    @staticmethod
    def mock_item_with_invalid_create_at() -> dict:
        return {"id": 12,
                "name": 213,
                "price": 10.02,
                "user_id": 1,
                "create_at": "w",
                "last_modified": 123.12}
    
    @staticmethod
    def mock_item_with_invalid_last_modified() -> dict:
        return {"id": 12,
                "name": 213,
                "price": 10.02,
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": "a"}