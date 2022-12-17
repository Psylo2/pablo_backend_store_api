import os
import stripe

from domain.entities.payment_entity import PaymentEntity
from application.interfaces.core.managers.language_interface import LanguageInterface
from infrastructure.interfaces.external_api.payments_interface import PaymentsApiInterface


class PaymentsAPI(PaymentsApiInterface):
    def __init__(self, language_manager: LanguageInterface):
        self.language_manager = language_manager
        self.__api_key = os.getenv("STRIPE_SECRET_KEY")

    def charge_payment(self, token: str, payment: PaymentEntity, email: str) -> dict:
        stripe.api_key = self.__api_key
        charge_payload = self._charge_payload(token=token, payment=payment, email=email)
        return stripe.Charge.create(**charge_payload)

    def refund_payment(self, payment: PaymentEntity) -> dict:
        stripe.api_key = self.__api_key
        refund_payload = self._refund_payload(payment=payment)
        return stripe.Refund.create(**refund_payload)

    @staticmethod
    def _convert_amount_to_cents(amount: int) -> int:
        return int(amount * 100)

    @staticmethod
    def _items_description(items: list) -> str:
        description = ""
        for item in items:
            description += f"({item['id']}:{item['title']}),"
        return description[:-1]

    def _get_currency_based_language(self) -> str:
        return self.language_manager.get('payment_currency')

    def _charge_payload(self, token: str, payment: PaymentEntity, email: str) -> dict:
        return {
            "amount": self._convert_amount_to_cents(amount=payment.amount),
            "currency": self._get_currency_based_language(),
            "description": self._items_description(items=payment.items),
            "receipt_email": email,
            "source": token}

    @staticmethod
    def _refund_payload(payment: PaymentEntity) -> dict:
        return {"charge": payment.transaction_id}
