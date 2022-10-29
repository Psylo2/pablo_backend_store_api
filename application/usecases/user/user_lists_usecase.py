from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.usecases.user.user_lists_interface import UserListsInterface

from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface


class UserListsUseCase(UserListsInterface):
    def __init__(self,
                 repository_queries: UserQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def allowed_users_list(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)

        allowed_users_list = self.repository_queries.find_by(key="blocked", value=False)
        return {"users": allowed_users_list}, 200

    def blocked_users_list(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)

        blocked_users_list = self.repository_queries.find_by(key="blocked", value=True)
        return {"users": blocked_users_list}, 200

    def all_users_list(self, jwt_data: dict) -> tuple:
        self._check_admin_privilege(jwt_data=jwt_data)
        all_users_list = self.repository_queries.fetch_all()
        return {"users": all_users_list}, 200

    def _check_admin_privilege(self, jwt_data: dict) -> None:
        if not jwt_data['is_admin']:
            raise AdminError(self.language_manager.get("admin_privilege"))
