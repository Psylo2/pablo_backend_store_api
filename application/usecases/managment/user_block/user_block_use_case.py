from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.usecases.managment.user_block_interface import UserBlockInterface
from application.exceptions import AdminError, UserError

from infrastructure.repositories.queries.user_queries import UserQueries


class UserBlockUseCase(UserBlockInterface):
    accepted_image_mimetype: set[str] = {'image/png', 'image/jpeg', 'image/pjpeg'}

    def __init__(self,
                 repository_queries: UserQueries,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 field_validation_manager: FieldsValidationInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.field_validation_manager = field_validation_manager

    def block_user(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        self._user_block_switch(jwt_data=jwt_data, data=data, block_value=True)
        return {"message": self.language_manager.get("user_blocked")}, 200

    def unblock_user(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        self._user_block_switch(jwt_data=jwt_data, data=data, block_value=False)
        return {"message": self.language_manager.get("user_unblocked")}, 200

    def _user_block_switch(self, jwt_data: dict, data: dict, block_value: bool) -> None:
        if not jwt_data['is_admin']:
            raise AdminError(self.language_manager.get("admin_privilege"))

        user = self.repository_queries.find_by(key="id", value=data['user_id'])
        if not user:
            raise UserError(self.language_manager.get("user_not_found"))

        user.blocked = block_value
        self.repository_queries.update(entity=user)
