from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.managment.promo_interface import PromoInterface

from infrastructure.interfaces.repositories.queries.subscriber_queries_interface import SubscriberQueriesInterface
from infrastructure.interfaces.repositories.queries.item_queries_interface import ItemQueriesInterface
from infrastructure.interfaces.external_api.email_interface import EmailApiInterface

T_SUBSCRIBER = TypeVar("T_SUBSCRIBER")
T_ITEM = TypeVar("T_ITEM")


EMAIL_SUBJECT = "ShoPPa Ads"
EMAIL_TEXT = ""

class PromoUseCase(PromoInterface):
    def __init__(self,
                 repository_queries: SubscriberQueriesInterface,
                 item_repository_queries: ItemQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 caesar_cipher: CaesarCipherInterface,
                 email_api: EmailApiInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.item_repository_queries = item_repository_queries
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.caesar_cipher = caesar_cipher
        self.email_api = email_api

    def send_ads(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        # if not jwt_data['is_admin']:
        #     raise AdminError(self.language_manager.get("admin_privilege"))

        item = self._get_item(data=data)
        subscribers = self.repository_queries.fetch_all_sorted_by(key="confirmed", value=True)
        if not subscribers:
            return {"message": "no registered subscribers"}, 200

        self._send_ads(item=item, subscribers=subscribers)
        return {"subscribers_amount": len(subscribers),
                "item": item.title}, 201

    def _get_item(self, data: dict[str, str]) -> T_ITEM:
        if not self.field_validation_manager.item_name_regex(name=data['item_title']):
            raise ValueError(self.language_manager.get("invalid_string"))

        item = self.item_repository_queries.find_by(key="title", value=data['item_title'])
        if not item:
            raise ValueError(self.language_manager.get("item_not_found"))

        return item

    def _get_subscribers_email(self) -> list[str]:
        subscribers = self.repository_queries.fetch_all()
        email_list = []

        for subscriber in subscribers:
            email = self.caesar_cipher.decrypt(text=subscriber.email)
            email_list.append(email)
        return email_list

    def _send_ads(self, item: T_ITEM, subscribers: list[T_SUBSCRIBER]) -> None:
        # TODO: html + link for promo
        link = "link to item page!"
        html = f'<html>Promo -> {item.title}, ' \
               f'display item details' \
               f'<a href="{link}">link to item page!</a></html>'

        for subscriber in subscribers:
            email = self.caesar_cipher.decrypt(text=subscriber.email)
            self.email_api.send_email(email=email, subject=EMAIL_SUBJECT, text=EMAIL_TEXT, html=html)

            subscriber.last_ad_sent_timestamp = self.repository_queries.insert_timestamp()
            self.repository_queries.update(entity=subscriber)
