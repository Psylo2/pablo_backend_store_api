from flask import request, url_for, render_template
from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.user.subscriber_interface import SubscriberInterface
from application.exceptions import UserError

from infrastructure.interfaces.repositories.queries.subscriber_queries_interface import SubscriberQueriesInterface
from infrastructure.interfaces.external_api.email_interface import EmailApiInterface

T_CONFIRMATION = TypeVar("T_CONFIRMATION")


EMAIL_SUBJECT = "Subscriber Confirmation"
EMAIL_TEXT = ""


class SubscriberUseCase(SubscriberInterface):
    def __init__(self,
                 repository_queries: SubscriberQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 caesar_cipher: CaesarCipherInterface,
                 email_api: EmailApiInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.caesar_cipher = caesar_cipher
        self.email_api = email_api

    def add_subscriber(self, data: dict) -> tuple[dict, int]:
        self._validate_data(data=data)
        confirm_data = {"email": self.caesar_cipher.encrypt(text=data['email'])}
        confirmation = self.repository_queries.save(data=confirm_data)
        self._send_email(email=data['email'], confirmation_id=confirmation.id)
        return {'message': self.language_manager.get("subscriber_registered").format(data['email'])}, 201

    def confirm_subscriber(self, data: dict) -> tuple[dict | str, int | None]:
        data = self.decrypt_confirmation_data(data=data)
        confirmation = self.repository_queries.find_by(key='id', value=data['confirmation_id'])

        if not confirmation:
            raise UserError(self.language_manager.get("conf_not_found"))

        if self.is_already_confirmed(confirmation=confirmation):
            raise UserError(self.language_manager.get("conf_reg_already"))

        return self.subscriber_page(data=data, confirmation=confirmation)

    def remove_subscriber(self, data: dict) -> tuple[dict, int]:
        self._validate_data(data=data)
        cesare_email = self.caesar_cipher.encrypt(data['email'])
        confirmation = self.repository_queries.find_by(key="email", value=cesare_email)

        if not confirmation:
            raise UserError(self.language_manager.get("conf_not_found"))

        self.repository_queries.remove(entity=confirmation)
        return {'message': self.language_manager.get("subscriber_removed")}, 200

    def _validate_data(self, data: dict) -> None:
        email = data['email']
        if not self.field_validation_manager.email_regex(email=email):
            raise ValueError(self.language_manager.get("email_error"))

    def _send_email(self, email: str, confirmation_id: str) -> None:
        link = request.url_root[:-1] + url_for(endpoint="subscriberresource",
                                               confirmation_id=self.caesar_cipher.encrypt(confirmation_id),
                                               email=self.caesar_cipher.encrypt(email))

        html = f'<html>Hello Subscriber, ' \
               f'Please click the link to confirm your subscription: ' \
               f'<a href="{link}">Email Confirmation</a></html>'

        self.email_api.send_email(email=email, subject=EMAIL_SUBJECT, text=EMAIL_TEXT, html=html)

    def subscriber_page(self, data: dict, confirmation: T_CONFIRMATION) -> tuple[str, None]:
        confirmation.confirm_timestamp = self.repository_queries.insert_timestamp()
        confirmation.confirmed = True
        self.repository_queries.update(entity=confirmation)

        return render_template("subscriber_page.html", email=data['email']), None

    @staticmethod
    def is_already_confirmed(confirmation: T_CONFIRMATION):
        return confirmation.confirmed

    def decrypt_confirmation_data(self, data: dict) -> dict:
        decrypted_data = {}
        for key, value in data.items():
            decrypted_data[key] = self.caesar_cipher.decrypt(text=value)

        return decrypted_data
