import json

from application.interfaces.core.managers.language_interface import LanguageInterface


class LanguageManager(LanguageInterface):
    language_mapper: dict[str, str] = {"US": "en-us",
                                       "RU": "ru-ru",
                                       "ES": "es-es"}

    def __init__(self):
        self.cached_strings = {}
        self.selected_language = None
        self.change_language('US')

    def get(self, name: str) -> str:
        return self.cached_strings.get(name)

    def refresh_cache(self) -> None:
        with open(f"application/core/strings/{self.selected_language}.json") as f:
            self.cached_strings = json.load(f)

    def change_language(self, selected_language: str) -> None:
        selected_language = self.language_mapper.get(selected_language, 'US')
        self.selected_language = selected_language
        self.refresh_cache()
