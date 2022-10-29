from abc import ABC, abstractmethod


class JWTConfigurationManagerInterface(ABC):

    @abstractmethod
    def check_if_token_in_blacklist(self, decrypted_token) -> bool:
        """Check if JWT Token is in BlackList"""
        ...

    @abstractmethod
    def add_claims_to_jwt(self, identity) -> dict:
        """Check if identity is Admin for ADMIN privileges"""
        ...
