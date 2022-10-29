from flask import request, url_for, render_template
from time import time
from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.user.confirmation_interface import ConfirmationInterface
from application.exceptions import UserError

from infrastructure.repositories.queries.confirmation_queries import ConfirmationRepository
from infrastructure.interfaces.external_api.email_interface import EmailApiInterface

T_CONFIRMATION = TypeVar("T_CONFIRMATION")


EMAIL_SUBJECT = "Registration Confirmation"
EMAIL_TEXT = ""


class ConfirmationUseCase(ConfirmationInterface):
    def __init__(self,
                 repository_queries: ConfirmationRepository,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 caesar_cipher: CaesarCipherInterface,
                 email_api: EmailApiInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.caesar_cipher = caesar_cipher
        self.email_api = email_api

    def send_email_confirmation(self, user_data: dict) -> None:
        data = {"user_id": user_data['id']}

        try:
            confirmation = self.repository_queries.save(data=data)
        except Exception as err:
            raise UserError(err)

        self._prepare_email_content(user_data=user_data, confirmation_id=confirmation.id)

    def _prepare_email_content(self, user_data: dict, confirmation_id: str) -> None:
        link = request.url_root[:-1] + url_for(endpoint="confirmationresource",
                                               confirmation_id=self.caesar_cipher.encrypt(confirmation_id),
                                               email=self.caesar_cipher.encrypt(user_data['email']),
                                               name=self.caesar_cipher.encrypt(user_data['name']))

        html = f'<html>Hello {user_data["name"].capitalize()}, ' \
               f'Please click the link to confirm your registration: ' \
               f'<a href="{link}">Email Confirmation</a></html>'

        self.email_api.send_email(email=user_data['email'],
                                  subject=EMAIL_SUBJECT,
                                  text=EMAIL_TEXT,
                                  html=html)

    def confirm(self, confirmation_data: dict) -> tuple:
        self.decrypt_confirmation_data(confirmation_data=confirmation_data)
        confirmation = self.repository_queries.find_by(key='id', value=confirmation_data['confirmation_id'])

        if not confirmation:
            raise UserError(self.language_manager.get("conf_not_found"))

        if self.is_confirmation_expired(confirmation=confirmation):
            raise UserError(self.language_manager.get("conf_expired"))

        if self.is_already_confirmed(confirmation=confirmation):
            raise UserError(self.language_manager.get("conf_reg_already"))

        return self.confirmation_page(confirmation_data=confirmation_data, confirmation=confirmation)

    def confirmation_page(self, confirmation_data: dict, confirmation: T_CONFIRMATION):
        confirmation.confirm_timestamp = self.repository_queries.insert_timestamp()
        confirmation.confirmed = True
        self.repository_queries.update(entity=confirmation)

        return render_template(
            "confirmation_page.html",
            email=confirmation_data['email'],
            name=confirmation_data['name'].capitalize()
        ), None

    @staticmethod
    def is_confirmation_expired(confirmation: T_CONFIRMATION) -> bool:
        return time() > confirmation.expired_at

    @staticmethod
    def is_already_confirmed(confirmation: T_CONFIRMATION) -> bool:
        return confirmation.confirmed

    def decrypt_confirmation_data(self, confirmation_data: dict) -> None:
        for key, value in confirmation_data.items():
            confirmation_data[key] = self.caesar_cipher.decrypt(text=value)

    def is_user_confirmed(self, user_id: int) -> bool:
        confirmation = self.repository_queries.find_by(key="user_id", value=user_id)
        return self.is_already_confirmed(confirmation=confirmation)
