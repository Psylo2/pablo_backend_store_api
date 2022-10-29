from unittest import TestCase
from pydantic.error_wrappers import ValidationError

from domain.entities.payment_entity import PaymentEntity


class TestPaymentEntity(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_entity = MockEntity()

    def test_entity_valid_payment_all_fields(self) -> None:
        payment = PaymentEntity(**self.mock_entity.mock_valid_payment_all_fields())
        self.assertTrue(expr=payment, msg="Valid payment")

    def test_entity_valid_payment_required_fields_only(self) -> None:
        payment = PaymentEntity(**self.mock_entity.mock_valid_payment_required_fields_only())
        self.assertTrue(expr=payment, msg="Valid payment")

    def test_entity_invalid_payment_id(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_id())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid id")

    def test_entity_invalid_payment_amount(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_amount())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid amount")

    def test_entity_invalid_payment_total_quantity(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_total_quantity())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid total_quantity")

    def test_entity_invalid_payment_user_id(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_user_id())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid user_id")

    def test_entity_invalid_payment_payment_at(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_payment_at())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid payment_at")

    def test_entity_invalid_payment_items(self) -> None:
        try:
            payment = PaymentEntity(**self.mock_entity.mock_payment_with_invalid_items())
        except ValidationError:
            payment = None
        self.assertFalse(expr=payment, msg="Invalid items")


class MockEntity:

    @staticmethod
    def mock_valid_payment_all_fields() -> dict:
        return {"id": 12,
                "amount": 12.1,
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_valid_payment_required_fields_only() -> dict:
        return {"amount": 12.1,
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_id() -> dict:
        return {"id": "a",
                "amount": 12.1,
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_amount() -> dict:
        return {"amount": "as",
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_total_quantity() -> dict:
        return {"amount": "as",
                "total_quantity": 5.5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_user_id() -> dict:
        return {"amount": 12.1,
                "total_quantity": 5,
                "user_id": "ar",
                "payment_at": 11.1,
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_payment_at() -> dict:
        return {"amount": 12.1,
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": "er",
                "items": []}

    @staticmethod
    def mock_payment_with_invalid_items() -> dict:
        return {"amount": 12.1,
                "total_quantity": 5,
                "user_id": 1,
                "payment_at": 11.1,
                "items": {}}
