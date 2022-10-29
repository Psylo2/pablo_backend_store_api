from abc import ABC, abstractmethod

class LanguageInterface(ABC):

    @abstractmethod
    def get(self, name) -> str:
        ...
