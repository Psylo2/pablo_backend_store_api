from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.usecases.managment.password_interface import PasswordInterface

from infrastructure.repositories.queries.user_queries import UserQueries


class PasswordUseCase(PasswordInterface):
    def __init__(self,
                 repository_queries: UserQueries,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface,
                 black_list_manager: set):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager
        self.black_list_manager = black_list_manager

    def get_password_configuration(self) -> tuple:
        if not data['is_admin']:
            return {"message": self.language_manager.get("admin_privilege")}, 401
        ...

    def authenticate_password(self, user_name: str, password: str) -> bool:
        user = self.repository_queries.find_by(key='username', value=user_name)
        is_valid_password = self.repository_queries.decrypt(str_field=password, byte_field=user.current_password)
        if is_valid_password:
            return True
        return False

    def fail_attempts(self, data: dict) -> bool:
        ...

    def password_complexity(self, data: dict) -> bool:
        ...

    def password_history(self, data: dict) -> bool:
        ...

    def password_dictionary(self, data: dict) -> bool:
        ...

    def _handle_oauth_passwords(self, user_name: str, timestamp: float) -> None:
        temp_password = self._generate_rand_password()
        password_data = {'username': user_name,
                         'last_change': timestamp,
                         'current_password': temp_password}
        self.repository_queries.save(data=password_data)

    def _generate_rand_password(self) -> bytes:
        ...
