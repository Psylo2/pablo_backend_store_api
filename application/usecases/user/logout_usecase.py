from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.usecases.user.logout_interface import LogoutInterface

from infrastructure.repositories.queries.user_queries import UserQueries


class LogoutUseCase(LogoutInterface):
    def __init__(self,
                 repository_queries: UserQueries,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 black_list_manager: set):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.black_list_manager = black_list_manager

    def user_logout(self, data: dict) -> tuple:
        user_jti = data['jti']
        self.black_list_manager.add(user_jti)
        return {"message":  self.language_manager.get("user_logout")}, 200
