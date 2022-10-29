from abc import ABC, abstractmethod

class TokenRefreshInterface(ABC):

    @abstractmethod
    def refresh_token(self, identity: any) -> tuple:
        ...
