from unittest import TestCase

from application.core.managers.language_manager import LanguageManager

class TestStringLanguage(TestCase):
    def setUpClass(cls) -> None:
        cls.language_manager = LanguageManager()

    def setUp(self) -> None:
        ...

    def test_get(self) -> None:
        ...

    def test_change_language(self) -> None:
        ...

    def tearDown(self) -> None:
        ...

    def tearDownClass(cls) -> None:
        ...

    def expected_result(self) -> any:
        ...
