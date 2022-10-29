from abc import ABC, abstractmethod


class CaesarCipherInterface(ABC):

    @abstractmethod
    def encrypt(self, text: str) -> str:
        ...

    @abstractmethod
    def decrypt(self, text: str) -> str:
        ...
