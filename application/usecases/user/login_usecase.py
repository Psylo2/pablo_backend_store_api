from flask_jwt_extended import create_access_token, create_refresh_token
from logging import Logger
from typing import TypeVar

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.user.login_interface import LoginInterface
from application.interfaces.usecases.user.confirmation_interface import ConfirmationInterface
from application.exceptions import UserError

from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface

T_USER = TypeVar("T_USER")


class LoginUseCase(LoginInterface):
    def __init__(self,
                 repository_queries: UserQueriesInterface,
                 logger: Logger,
                 confirmation_use_case: ConfirmationInterface,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 caesar_cipher: CaesarCipherInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.confirmation_use_case = confirmation_use_case
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.caesar_cipher = caesar_cipher

    def user_login(self, user_data: dict) -> tuple:
        user = self._verify_user(user_data=user_data)

        if not user:
            raise UserError(self.language_manager.get("invalid_credentials"))

        if not self.is_user_confirmed(user=user):
            raise UserError(self.language_manager.get("user_not_confirmed"))

        self._update_login_time(user=user)
        return self._login_payload(user=user), 200

    def is_user_confirmed(self, user: T_USER):
        return self.confirmation_use_case.is_user_confirmed(user_id=user.id)

    def _find_user(self, user_data: dict) -> T_USER | None:
        email = self.caesar_cipher.encrypt(text=user_data['email'])
        return self.repository_queries.find_by(key='email', value=email)

    def _verify_user(self, user_data: dict) -> T_USER | None:
        user = self._find_user(user_data=user_data)
        if not user:
            return None

        password_verified = self._verify_password(user_data=user_data, user=user)
        if password_verified:
            return user

    def _verify_password(self, user_data: dict, user: T_USER) -> bool:
        password = user_data['password']
        return False if self.repository_queries.decrypt(str_field="", byte_field=user.password) else \
            self.repository_queries.decrypt(str_field=password, byte_field=user.password)

    def _update_login_time(self, user: T_USER) -> None:
        user.last_login = self.repository_queries.insert_timestamp()
        self.repository_queries.update(entity=user)

    @staticmethod
    def _login_payload(user: T_USER) -> dict:
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
