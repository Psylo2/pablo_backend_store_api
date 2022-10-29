from unittest import TestCase
from pydantic.error_wrappers import ValidationError

from domain.entities.cart_entity import CartEntity


class TestCartEntity(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_entity = MockEntity()

    def test_entity_valid_cart_all_fields(self) -> None:
        cart = CartEntity(**self.mock_entity.mock_valid_cart_all_fields())
        self.assertTrue(expr=cart, msg="Valid cart")

    def test_entity_valid_cart_required_fields_only(self) -> None:
        cart = CartEntity(**self.mock_entity.mock_valid_cart_required_fields_only())
        self.assertTrue(expr=cart, msg="Valid cart")

    def test_entity_invalid_cart_id(self) -> None:
        try:
            cart = CartEntity(**self.mock_entity.mock_cart_with_invalid_id())
        except ValidationError:
            cart = None
        self.assertFalse(expr=cart, msg="Invalid id")

    def test_entity_invalid_cart_items(self) -> None:
        try:
            cart = CartEntity(**self.mock_entity.mock_cart_with_invalid_items())
        except ValidationError:
            cart = None
        self.assertFalse(expr=cart, msg="Invalid items")

    def test_entity_invalid_cart_user_id(self) -> None:
        try:
            cart = CartEntity(**self.mock_entity.mock_cart_with_invalid_user_id())
        except ValidationError:
            cart = None
        self.assertFalse(expr=cart, msg="Invalid user_id")

    def test_entity_invalid_cart_create_at(self) -> None:
        try:
            cart = CartEntity(**self.mock_entity.mock_cart_with_invalid_create_at())
        except ValidationError:
            cart = None
        self.assertFalse(expr=cart, msg="Invalid created_at")

    def test_entity_invalid_cart_last_modified(self) -> None:
        try:
            cart = CartEntity(**self.mock_entity.mock_cart_with_invalid_create_at())
        except ValidationError:
            cart = None
        self.assertFalse(expr=cart, msg="Invalid last_modified")


class MockEntity:

    @staticmethod
    def mock_valid_cart_all_fields() -> dict:
        return {"id": 12,
                "items": [],
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_valid_cart_required_fields_only() -> dict:
        return {"items": [],
                "user_id": 1}

    @staticmethod
    def mock_cart_with_invalid_id() -> dict:
        return {"id": "a",
                "name": "cart",
                "price": 10.02,
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_cart_with_invalid_items() -> dict:
        return {"id": 12,
                "items": {},
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_cart_with_invalid_user_id() -> dict:
        return {"id": 12,
                "items": [],
                "user_id": "e",
                "create_at": 11.1,
                "last_modified": 123.12}

    @staticmethod
    def mock_cart_with_invalid_create_at() -> dict:
        return {"id": 12,
                "items": [],
                "user_id": 1,
                "create_at": "w",
                "last_modified": 123.12}

    @staticmethod
    def mock_cart_with_invalid_last_modified() -> dict:
        return {"id": 12,
                "items": [],
                "user_id": 1,
                "create_at": 11.1,
                "last_modified": "a"}
