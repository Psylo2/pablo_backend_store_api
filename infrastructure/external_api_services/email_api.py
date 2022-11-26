import os
import requests
from requests import Response

from infrastructure.interfaces.external_api.email_interface import EmailApiInterface
from application.interfaces.core.managers.language_interface import LanguageInterface


class EmailAPI(EmailApiInterface):
    def __init__(self, language_manager: LanguageInterface):
        self.language_manager = language_manager
        self._email_api_domain = os.environ.get("EMAIL_API_DOMAIN")
        self.__email_api_key = os.environ.get("EMAIL_API_KEY")

    def send_email(self, email: str, subject: str, text: str, html: str) -> Response:
        self.validate_email_api_connectivity()
        post_request_content = self.post_request_content(email=email, subject=subject, text=text, html=html)
        response = requests.post(**post_request_content)
        return self.valid_response(response=response)

    @property
    def title(self) -> str:
        return "ShoPPA store"

    @property
    def do_not_replay_email(self) -> str:
        return f"do-not-reply@shoppa.pro"

    def validate_email_api_connectivity(self) -> None:
        if not self._email_api_domain or not self.__email_api_key:
            raise EmailAPIException(self.language_manager.get("mailgun_failed_load_api"))

    @property
    def email_api_url(self) -> str:
        return f"https://api.mailgun.net/v3/{self._email_api_domain}/messages"

    @property
    def __api_auth(self) -> tuple:
        return "api", self.__email_api_key

    def generate_email_data(self, email: str, subject: str, text: str, html: str) -> dict:
        return {"from": f"{self.title} <{self.do_not_replay_email}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html}

    def post_request_content(self, email: str, subject: str, text: str, html: str) -> dict:
        data = self.generate_email_data(email=email, subject=subject, text=text, html=html)
        return {"url": self.email_api_url,
                "auth": self.__api_auth,
                "data": data}

    def valid_response(self, response: Response) -> Response:
        if response.status_code != 200:
            raise EmailAPIException(self.language_manager.get("mailgun_error_send_email"))
        return response


class EmailAPIException(Exception):
    ...
