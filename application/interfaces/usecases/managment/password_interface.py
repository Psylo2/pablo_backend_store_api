from abc import ABC, abstractmethod

class PasswordInterface(ABC):

    @abstractmethod
    def authenticate_password(self, user_name: str, password: str) -> bool:
        ...

    @abstractmethod
    def get_password_configuration(self) -> tuple:
        ...

    @abstractmethod
    def fail_attempts(self, data: dict) -> bool:
        ...

    @abstractmethod
    def password_complexity(self, data: dict) -> bool:
        ...

    @abstractmethod
    def password_history(self, data: dict) -> bool:
        ...

    @abstractmethod
    def password_dictionary(self, data: dict) -> bool:
        ...

    @abstractmethod
    def _handle_oauth_passwords(self, user_name: str, timestamp: float) -> None:
        ...
