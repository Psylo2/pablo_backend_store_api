from abc import ABC, abstractmethod
from flask import Response

class OAuthInterface(ABC):

    @abstractmethod
    def user_login(self) -> Response:
        ...

    @abstractmethod
    def user_authorize(self) -> tuple:
        ...

    @abstractmethod
    def get_access_token(self) -> str:
        ...

    @abstractmethod
    def _user_authorize_payload(self) -> dict:
        ...

    @abstractmethod
    def _user_payload(self, user) -> dict:
        ...

    @abstractmethod
    def _user_login_payload(self, user, access_token: str, refresh_token: str) -> dict:
        ...

    @abstractmethod
    def _new_user(self, user_name: str) -> type:
        ...

    @abstractmethod
    def _new_user_payload(self, user_name: str) -> dict:
        ...
