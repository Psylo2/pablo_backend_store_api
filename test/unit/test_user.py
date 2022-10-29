from unittest import TestCase
from pydantic.error_wrappers import ValidationError

from domain.entities.user_entity import UserEntity


class TestUserEntity(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_entity = MockEntity()

    def test_entity_valid_user_all_fields(self) -> None:
        user = UserEntity(**self.mock_entity.mock_valid_user_all_fields())
        self.assertTrue(expr=user, msg="Valid User")

    def test_entity_valid_user_required_fields_only(self) -> None:
        user = UserEntity(**self.mock_entity.mock_valid_user_required_fields_only())
        self.assertTrue(expr=user, msg="Valid User")

    def test_entity_invalid_id(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_id())
        except ValidationError:
            user = None
        self.assertFalse(expr=user, msg="Invalid id")

    def test_entity_invalid_create_at(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_create_at())
        except ValidationError or AssertionError:
            user = None
        self.assertFalse(expr=user, msg="Invalid create_t")

    def test_entity_invalid_last_login(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_last_login())
        except ValidationError:
            user = None
        self.assertFalse(expr=user, msg="Invalid last_login")

    def test_entity_invalid_name(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_name())
        except ValidationError:
            user = None
        self.assertFalse(expr=user, msg="Invalid name")

    def test_entity_invalid_email(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_email())
        except ValidationError:
            user = None
        self.assertFalse(expr=user, msg="Invalid email")

    def test_entity_invalid_password(self) -> None:
        try:
            user = UserEntity(**self.mock_entity.mock_user_with_invalid_password())
        except ValidationError:
            user = None
        self.assertFalse(expr=user, msg="Invalid password")

class MockEntity:

    @staticmethod
    def mock_valid_user_all_fields() -> dict:
        return {"id": 1,
                "name": "user",
                "email": bytes("user@email.co.il".encode("UTF-8")),
                "password": bytes("user".encode("UTF-8")),
                "create_at": 11.1,
                "last_login": 12.1}

    @staticmethod
    def mock_valid_user_required_fields_only() -> dict:
        return {"name": "user",
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "password": bytes("user".encode("UTF-8"))}

    @staticmethod
    def mock_user_with_invalid_id() -> dict:
        return {"id": "a",
                "name": "user",
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "create_at": 11.1,
                "last_login": 12.1}

    @staticmethod
    def mock_user_with_invalid_create_at() -> dict:
        return {"name": "user",
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "password": bytes("user".encode("UTF-8")),
                "create_at": "a",
                "last_login": 12.1}

    @staticmethod
    def mock_user_with_invalid_last_login() -> dict:
        return {"name": "user",
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "password": bytes("user".encode("UTF-8")),
                "create_at": 1.1,
                "last_login": "y"}

    @staticmethod
    def mock_user_with_invalid_name() -> dict:
        return {"id": "a",
                "name": 234,
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "password": bytes("user".encode("UTF-8")),
                "create_at": 11.1,
                "last_login": 12.1}

    @staticmethod
    def mock_user_with_invalid_email() -> dict:
        return {"id": "a",
                "name": "234",
                "email": "user@email.co.ill",
                "password": bytes("user".encode("UTF-8")),
                "create_at": 11.1,
                "last_login": 12.1}

    @staticmethod
    def mock_user_with_invalid_password() -> dict:
        return {"id": "a",
                "name": "234",
                "email": bytes("user@email.co.ill".encode("UTF-8")),
                "password": "user",
                "create_at": 11.1,
                "last_login": 12.1}
