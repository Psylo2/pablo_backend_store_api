import traceback
from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface
from application.interfaces.usecases.user.register_interface import RegisterInterface
from application.interfaces.usecases.user.confirmation_interface import ConfirmationInterface
from application.exceptions import UserError

from infrastructure.repositories.queries.user_queries import UserQueries
from infrastructure.external_api_services.email_api import EmailAPIException


class RegisterUseCase(RegisterInterface):
    def __init__(self,
                 repository_queries: UserQueries,
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

    def user_register(self, user_data: dict) -> tuple:
        if self._user_exists(user_data=user_data):
            raise UserError(self.language_manager.get("user_name_exists"))

        if not self._is_password_valid(user_data=user_data):
            raise UserError(self.language_manager.get("password_error"))

        if not self._is_email_valid(user_data=user_data):
            raise UserError(self.language_manager.get("email_error"))

        return self._user_register(user_data=user_data)

    def _user_exists(self, user_data: dict) -> bool:
        user_by_name = self.repository_queries.find_by(key='name', value=user_data['name'])
        email = self.caesar_cipher.encrypt(text=user_data['email'])
        user_by_email = self.repository_queries.find_by(key='name', value=email)
        return True if user_by_name or user_by_email else False

    def _is_password_valid(self, user_data: dict) -> bool:
        password = user_data.get('password')
        return self.field_validation_manager.password_regex(password=password)

    def _is_email_valid(self, user_data: dict) -> bool:
        email = user_data.get('email')
        return self.field_validation_manager.email_regex(email=email)

    def _user_register(self, user_data: dict) -> tuple[dict, int]:
        data = self._enrich_user_data(user_data=user_data)

        try:
            user = self.repository_queries.save(data=data)
            user_data['id'] = user.id
            self.confirmation_use_case.send_email_confirmation(user_data=user_data)

            return {'message': self.language_manager.get("user_registered").format(user_data['email'])}, 201

        except EmailAPIException as e:  # failed confirmation email
            self.repository_queries.remove(entity=user)
            return {"message": str(e)}, 500

        except Exception as err:  # failed to save user to db
            traceback.print_exc()
            self.repository_queries.remove(entity=user)
            return {"message": self.language_manager.get("user_internal_server_error")}, 500

    def _enrich_user_data(self, user_data: dict) -> dict:
        return {'name': user_data['name'],
                'password': self.repository_queries.encrypt(user_data['password']),
                'email': self.caesar_cipher.encrypt(user_data['email']),
                'create_at': self.repository_queries.insert_timestamp(),
                'blocked': False}
