from abc import abstractmethod


class RepositoryInterface:

    @abstractmethod
    def add_to_repository(self) -> None:
        ...

    @abstractmethod
    def remove_from_repository(self) -> None:
        ...

    @abstractmethod
    def update_repository(self) -> None:
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        ...
