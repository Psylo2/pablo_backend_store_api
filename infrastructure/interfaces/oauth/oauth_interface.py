from abc import ABC, abstractmethod
from flask_oauthlib.client import OAuth, OAuthRemoteApp

class OAuthClientInterface(ABC):

    @property
    @abstractmethod
    def oauth(self) -> OAuth:
        ...

    @property
    @abstractmethod
    def remote_app(self) -> OAuthRemoteApp:
        ...

    @remote_app.setter
    @abstractmethod
    def remote_app(self, remote_app: OAuthRemoteApp):
        ...

    @abstractmethod
    def apply_oauth_settings(self) -> None:
        ...

    @abstractmethod
    def set_oauth_setting(self) -> dict:
        ...
