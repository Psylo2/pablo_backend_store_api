from abc import ABC, abstractmethod


class FieldsValidationInterface(ABC):

    @abstractmethod
    def email_regex(self, email: str) -> bool:
        """Regex Formula for User's Email
        first not dot,
        besides of '@' no dots,
        no more than 2 dots after '@',
        don't finish with dot"""
        ...

    @abstractmethod
    def username_regex(self, string: str) -> bool:
        """Regex Formula for User's Username
        don't start with digits and no digits only
        4 to 12 length"""
        ...

    @abstractmethod
    def password_regex(self, password: str) -> bool:
        """Regex Formula for User's Password
        at least: 2 Upper, 2 Lower, 4 Digits, 1 Special
        no more than 1 special"""
        ...

    @abstractmethod
    def item_name_regex(self, name: str) -> bool:
        """Regex Formula Item Name
        accepted only alphanumeric
        don't start with digit
        don't finish with '_'
        length 3-12
        """
        ...

    @abstractmethod
    def _sanitizer(self, string: str) -> bool:
        """REGEX Formula for Message control.
        don't start with '< {
        don't end with '> }
        no less than 3 character
        """
        ...
