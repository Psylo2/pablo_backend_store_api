from flask_jwt_extended import create_access_token
from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.usecases.user.token_refresh_interface import TokenRefreshInterface

from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface


class TokenRefreshUseCase(TokenRefreshInterface):
    def __init__(self,
                 repository_queries: UserQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager

    def refresh_token(self, identity: any) -> tuple:
        new_token = create_access_token(identity=identity, fresh=False)
        return {"access_token": new_token}, 200
