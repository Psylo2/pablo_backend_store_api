from abc import ABC, abstractmethod

class PromoInterface(ABC):

    @abstractmethod
    def send_ads(self, jwt_data: dict, data: dict) -> tuple[dict, int]:
        ...
