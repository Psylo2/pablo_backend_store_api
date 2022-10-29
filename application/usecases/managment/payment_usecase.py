from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.managment.payment_interface import PaymentInterface
from application.exceptions import AdminError, CartError, PaymentError

from infrastructure.interfaces.repositories.queries.payment_queries_interface import PaymentQueriesInterface
from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface
from infrastructure.interfaces.repositories.queries.item_queries_interface import ItemQueriesInterface
from infrastructure.interfaces.repositories.queries.cart_queries_interface import CartQueriesInterface
from infrastructure.interfaces.external_api.payments_interface import PaymentsApiInterface


T_ITEM = TypeVar("T_ITEM")
T_PAYMENT = TypeVar("T_PAYMENT")
T_CHARGE = TypeVar("T_CHARGE")


class PaymentUseCase(PaymentInterface):
    def __init__(self,
                 repository_queries: PaymentQueriesInterface,
                 cart_repository_queries: CartQueriesInterface,
                 item_repository_queries: ItemQueriesInterface,
                 user_repository_queries: UserQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 black_list_manager: set,
                 caesar_cipher: CaesarCipherInterface,
                 payments_api: PaymentsApiInterface):
        self.repository_queries = repository_queries
        self.cart_repository_queries = cart_repository_queries
        self.item_repository_queries = item_repository_queries
        self.user_repository_queries = user_repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.black_list_manager = black_list_manager
        self.caesar_cipher = caesar_cipher
        self.payments_api = payments_api

    def payment(self, identity: any, data: dict) -> tuple:
        cart = self.cart_repository_queries.find_by(key='user_id', value=identity)
        if not cart:
            raise CartError(self.language_manager.get("cart_not_found"))

        items = []
        for item_dict in cart.items:
            item = self.item_repository_queries.find_by(key="id", value=item_dict['id'])
            if item.sold:
                continue

            item.sold = True
            item.user_id = identity
            item.last_modified = self.repository_queries.insert_timestamp()
            items.append(item)

        payment_data = {
            "amount": self._calculate_amount(items=items),
            "total_quantity": len(items),
            "user_id": identity,
            "items": [item.to_dict() for item in items],
            "state": "pending",
            "payment_at": self.repository_queries.insert_timestamp()
        }
        payment = self.repository_queries.save(data=payment_data)
        user = self.user_repository_queries.find_by(key="id", value=identity)
        email = self.caesar_cipher.decrypt(text=user.email)
        charge = self.payments_api.charge_payment(token=data['token'], payment=payment, email=email)
        self._verify_transaction(charge=charge)

        payment.state = "paid"
        payment.transaction_id = charge['id']
        self.repository_queries.update(entity=payment)
        [self.item_repository_queries.update(item) for item in items]
        self.cart_repository_queries.remove(entity=cart)

        return payment.to_dict(), 200

    def full_refund(self, identity: any, data: dict) -> tuple:
        transaction_id = data['transaction_id']
        payment = self.repository_queries.find_by(key="transaction_id", value=transaction_id)
        self._validate_refund(identity=identity, transaction_id=transaction_id, payment=payment)

        refund = self.payments_api.refund_payment(payment=payment)
        self._verify_transaction(charge=refund)

        payment.state = "refund"
        payment.refund_at = self.repository_queries.insert_timestamp()
        payment.last_modified = self.repository_queries.insert_timestamp()
        payment.transaction_id = refund['id']
        self.repository_queries.update(entity=payment)

        for item in payment.items:
            item = self.item_repository_queries.find_by(key="id", value=item['id'])
            item.user_id = None
            item.sold = False
            item.last_modified = self.repository_queries.insert_timestamp()
            self.item_repository_queries.update(entity=item)

        return payment.to_dict(), 200

    def get_user_payments(self, identity: any) -> tuple:
        user_payments = self.repository_queries.fetch_all_sorted_by(key="user_id", value=identity)
        user_payments = [payment for payment in user_payments if payment.state != "refund"]
        return {"payments": user_payments}, 200

    def get_user_refund(self, identity: any) -> tuple:
        user_payments = self.repository_queries.fetch_all_sorted_by(key="user_id", value=identity)
        user_refunds = [payment for payment in user_payments if payment.state == "refund"]
        return {"refunds": user_refunds}, 200

    def all_payments(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)
        all_payments = self.repository_queries.fetch_all()
        return {"all_payments": all_payments}, 200

    def paid_payments(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)
        paid_payments = self.repository_queries.fetch_all_sorted_by(key="state", value="paid")
        return {"paid_payments": paid_payments}, 200

    def pending_payments(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)
        pending_payments = self.repository_queries.fetch_all_sorted_by(key="state", value="pending")
        return {"pending_payments": pending_payments}, 200

    def fail_payments(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)
        fail_payments = self.repository_queries.fetch_all_sorted_by(key="state", value="fail")
        return {"fail_payments": fail_payments}, 200

    def _check_admin_privilege(self, jwt_data: dict) -> None:
        if not jwt_data['is_admin']:
            raise AdminError(self.language_manager.get("admin_privilege"))

    @staticmethod
    def _calculate_amount(items: list[T_ITEM]) -> int:
        return sum(item.new_price for item in items)

    def _validate_refund(self, identity: any, transaction_id: str, payment: T_PAYMENT) -> None:
        if not payment:
            raise PaymentError(self.language_manager.get("transaction_not_found").format(transaction_id))
        if payment.user_id != identity:
            raise ValueError

    def _verify_transaction(self, charge: T_CHARGE) -> None:
        if charge.status != "succeeded":
            raise PaymentError(self.language_manager.get("refund_error"))
