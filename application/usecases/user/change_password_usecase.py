from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.usecases.user.change_password_interface import ChangePasswordInterface
from application.interfaces.usecases.managment.password_interface import PasswordInterface

from infrastructure.repositories.queries.user_queries import UserQueries


class ChangePasswordUseCase(ChangePasswordInterface):
    def __init__(self,
                 repository_queries: UserQueries,
                 logger: Logger,
                 password_use_case: PasswordInterface,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.password_use_case = password_use_case
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def change_password(self, data: dict) -> tuple:
        ...
