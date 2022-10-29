from abc import ABC, abstractmethod

class SubscriberInterface(ABC):

    @abstractmethod
    def confirm_subscriber(self, data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def add_subscriber(self, data: dict) -> tuple[dict, int]:
        ...

    @abstractmethod
    def remove_subscriber(self, data: dict) -> tuple[dict, int]:
        ...
