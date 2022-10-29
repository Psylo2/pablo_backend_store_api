from abc import ABC, abstractmethod


class AppConfigurationInterface(ABC):

    @property
    @abstractmethod
    def app(self):
        ...

    @property
    @abstractmethod
    def repository(self):
        ...

    @abstractmethod
    def apply_production_configurations(self) -> None:
        ...

    @abstractmethod
    def repository_init_app(self) -> None:
        ...

    @abstractmethod
    def repository_create_all_tables(self) -> None:
        ...

    @abstractmethod
    def configure_file_log(self) -> None:
        ...

    @abstractmethod
    def configure_console_log(self) -> None:
        ...
