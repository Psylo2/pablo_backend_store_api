import os
from time import time
from logging import Logger
from typing import TypeVar
from flask import request, url_for, render_template

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.user.change_password_interface import ChangePasswordInterface
from application.interfaces.usecases.managment.password_interface import PasswordInterface
from application.exceptions import UserError, PasswordError

from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface
from infrastructure.interfaces.repositories.queries.password_queries_interface import PasswordQueriesInterface
from infrastructure.interfaces.external_api.email_interface import EmailApiInterface

T_PASSWORD = TypeVar("T_PASSWORD")
T_USER = TypeVar("T_USER")

EMAIL_SUBJECT = "Change Password Confirmation"
EMAIL_TEXT = ""


class ChangePasswordUseCase(ChangePasswordInterface):
    def __init__(self,
                 repository_queries: PasswordQueriesInterface,
                 user_repository_queries: UserQueriesInterface,
                 logger: Logger,
                 password_use_case: PasswordInterface,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 caesar_cipher: CaesarCipherInterface,
                 email_api: EmailApiInterface):
        self.repository_queries = repository_queries
        self.user_repository_queries = user_repository_queries
        self.logger = logger
        self.password_use_case = password_use_case
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.caesar_cipher = caesar_cipher
        self.email_api = email_api

    def send_confirmation_email(self, data: dict) -> tuple:
        self._validate_email(data=data)
        email = self.caesar_cipher.encrypt(text=data['email'])
        user = self.user_repository_queries.find_by(key="email", value=email)

        if not user:
            raise UserError(self.language_manager.get("user_not_found"))

        try:
            password_model = self.repository_queries.find_by(key="user_id", value=user.id)
            if not password_model:
                password_model = self.repository_queries.save(data={"user_id": user.id})

            self._enrich_password_model_to_confirm(password_model=password_model, user=user)

            user.password = self.user_repository_queries.encrypt(str_field="")

            self.repository_queries.update(entity=password_model)
            self.user_repository_queries.update(entity=user)

        except Exception as err:
            raise UserError(err)

        self._send_email(email=data['email'], confirmation_id=password_model.id)
        return {'message': self.language_manager.get("user_password_confirmation")}, 201

    def confirm_email(self, data: dict) -> tuple:
        encrypted_email = data['email']
        self._decrypt_confirmation_data(confirmation_data=data)

        confirmation = self.repository_queries.find_by(key='id', value=data['confirmation_id'])

        if not confirmation:
            raise UserError(self.language_manager.get("conf_not_found"))

        if self._is_confirmation_expired(confirmation=confirmation):
            raise UserError(self.language_manager.get("conf_expired"))

        if self._is_already_confirmed(confirmation=confirmation):
            raise UserError(self.language_manager.get("conf_reg_already"))

        return self._confirmation_page(email=encrypted_email, confirmation=confirmation)

    def change_password(self, data: dict) -> tuple:
        self._decrypt_data(data=data)
        self._validate_change_password_data(data=data)

        confirmation_id = data['confirmation']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise PasswordError(self.language_manager.get("passwords_not_match"))

        password_model = self.repository_queries.find_by(key="id", value=confirmation_id)
        if not password_model:
            raise UserError(self.language_manager.get("user_not_found"))

        user = self.user_repository_queries.find_by(key="id", value=password_model.user_id)

        if not user:
            raise UserError(self.language_manager.get("user_not_found"))

        password_model.changed_password_timestamp = self.repository_queries.insert_timestamp()

        self._check_password_history(password=password, password_model=password_model)
        user.password = self.user_repository_queries.encrypt(str_field=password)

        self.repository_queries.update(entity=password_model)
        self.user_repository_queries.update(entity=user)

        return {'message': self.language_manager.get("password_changed")}, 201

    def _decrypt_confirmation_data(self, confirmation_data: dict) -> None:
        for key, value in confirmation_data.items():
            confirmation_data[key] = self.caesar_cipher.decrypt(text=value)

    def _enrich_password_model_to_confirm(self, password_model: T_PASSWORD, user: T_USER) -> None:
        password_model.confirmed = False
        self._handle_password_history_size(password_model=password_model)
        password_model.password_history.append(user.password)
        password_model.expired_at = int(time()) + int(os.environ.get('PASSWORD_EXP_DELTA'))

    @staticmethod
    def _handle_password_history_size(password_model: T_PASSWORD) -> None:
        if len(password_model.password_history) == 3:
            password_model.password_history.pop()

    def _check_password_history(self, password: str, password_model: T_PASSWORD) -> None:
        for old_password in password_model.password_history:
            if self.user_repository_queries.decrypt(str_field=password, byte_field=old_password):
                raise PasswordError(self.language_manager.get("password_in_history"))

        self._handle_password_history_size(password_model=password_model)

    def _validate_email(self, data: dict) -> None:
        if not self.field_validation_manager.email_regex(email=data['email']):
            raise ValueError(self.language_manager.get("email_error"))

    def _validate_change_password_data(self, data: dict) -> None:
        if not self.field_validation_manager.password_regex(password=data['password']):
            raise ValueError(self.language_manager.get("password_error"))

    def _send_email(self, email: str, confirmation_id: str) -> None:
        link = request.url_root[:-1] + url_for(endpoint="changepasswordresource",
                                               confirmation_id=self.caesar_cipher.encrypt(confirmation_id),
                                               email=self.caesar_cipher.encrypt(email))

        html = f'<html>Hello, ' \
               f'Please click the link to change your password: ' \
               f'<a href="{link}">Change Password</a></html>'

        self.email_api.send_email(email=email, subject=EMAIL_SUBJECT, text=EMAIL_TEXT, html=html)

    def _confirmation_page(self, email: str, confirmation: T_PASSWORD):
        confirmation.confirm_timestamp = self.repository_queries.insert_timestamp()
        confirmation.confirmed = True
        self.repository_queries.update(entity=confirmation)
        self.logger.info(f"Confirmation ID {confirmation.id} status: Success.")

        return render_template(
            "change_password_confirmation_page.html",
            confirmation=confirmation.id
        ), None

    @staticmethod
    def _is_confirmation_expired(confirmation: T_PASSWORD) -> bool:
        return time() > confirmation.expired_at

    @staticmethod
    def _is_already_confirmed(confirmation: T_PASSWORD) -> bool:
        return confirmation.confirmed

    def _decrypt_data(self, data: dict) -> None:
        for key, value in data.items():
            data[key] = self.caesar_cipher.decrypt(text=value)

    def _is_user_confirmed(self, user_id: int) -> bool:
        confirmation = self.repository_queries.find_by(key="user_id", value=user_id)
        return self.is_already_confirmed(confirmation=confirmation)
