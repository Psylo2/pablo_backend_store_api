from flask_oauthlib.contrib.apps import github
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import Response, g
from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.usecases.managment.oauth_interface import OAuthInterface
from application.interfaces.usecases.managment.password_interface import PasswordInterface

from infrastructure.interfaces.repositories.queries.user_queries_interface import UserQueriesInterface


class GithubOauthUseCase(OAuthInterface):
    def __init__(self,
                 repository_queries: UserQueriesInterface,
                 logger: Logger,
                 language_manager: LanguageInterface,
                 black_list_manager: set,
                 password_service: PasswordInterface,
                 github_service: github):
        self.repository_queries = repository_queries
        self.logger = logger
        self.language_manager = language_manager
        self.black_list_manager = black_list_manager
        self.password_service = password_service
        self.github_service = github_service

        self.github_service.remote_app.tokengetter(f=self.get_access_token)
        self._url_authorized = "http://localhost:5000/login/github/authorized/thank_you"

    def user_login(self) -> Response:
        return self.github_service.remote_app.authorize(callback=self._url_authorized)

    def user_authorize(self) -> tuple:
        resp_data = self.github_service.remote_app.authorized_response()
        if not resp_data and not resp_data.get("access_token"):
            return self.error_response(data=resp_data), 400

        g.access_token = resp_data['access_token']
        return self._user_authorize_payload(), 200

    def _user_authorize_payload(self) -> dict:
        username = github.get('user', {}).get('login')
        user = self.repository_queries.find_by(key='name', value=username)
        if not user:
            user = self._new_user(user_name=username)

        return self._user_payload(user=user)

    def _user_payload(self, user) -> dict:
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return self._user_login_payload(user=user, access_token=access_token, refresh_token=refresh_token)

    def _user_login_payload(self, user, access_token: str, refresh_token: str) -> dict:
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "username": user.username,
                "id": user.id,
                "email": user.email}

    def _new_user(self, user_name: str) -> type:
        timestamp = self.repository_queries.insert_timestamp()
        user_data = self._new_user_payload(user_name=user_name)
        user = self.repository_queries.save(data=user_data)
        self.password_service._handle_oauth_passwords(user_name=user.name, timestamp=timestamp)
        return user

    def _new_user_payload(self, user_name: str) -> dict:
        return {'name': user_name,
                'email': os.urandom(8).hex(),
                'create_at': timestamp,
                'last_login': timestamp}

    def get_access_token(self) -> str:
        if 'access_token' in g:
            return g.access_token
