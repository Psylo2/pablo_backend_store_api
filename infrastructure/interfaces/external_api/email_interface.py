from abc import ABC, abstractmethod
from requests import Response


class EmailApiInterface(ABC):

    @abstractmethod
    def send_email(self, email: str, subject: str, text: str, html: str) -> Response:
        ...
