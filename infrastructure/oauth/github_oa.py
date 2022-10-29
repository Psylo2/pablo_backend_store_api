import os
from flask_oauthlib.client import OAuth, OAuthRemoteApp

from infrastructure.interfaces.oauth.oauth_interface import OAuthClientInterface


class GitHubOAuth(OAuthClientInterface):
    def __init__(self, oauth: OAuth):
        self._oauth = oauth
        self._remote_app = None
        self.apply_oauth_settings()

    @property
    def oauth(self) -> OAuth:
        return self._oauth

    @property
    def remote_app(self) -> OAuthRemoteApp:
        return self._remote_app

    @remote_app.setter
    def remote_app(self, remote_app: OAuthRemoteApp):
        self._remote_app = remote_app

    def apply_oauth_settings(self) -> None:
        github_oauth_setting = self.set_oauth_setting()
        self.remote_app = self.oauth.remote_app(name="ShoPPA", **github_oauth_setting)

    def set_oauth_setting(self) -> dict:
        return {
            "consumer_key": os.getenv("GITHUB_CONSUMER_KEY"),
            "consumer_secret": os.getenv("GITHUB_CONSUMER_SECRET"),
            "request_token_params": {"scope": "user:email"},
            "base_url": "https://api.github.com/",
            "request_token_url": None,
            "access_token_method": "POST",
            "access_token_url": "https://github.com/login/oauth/access_token",
            "authorize_url": "https://github.com/login/oauth/authorize"
        }
