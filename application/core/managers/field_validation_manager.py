import re

from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface


class FieldsValidationManager(FieldsValidationInterface):
    _sanitizer_reg = r"^([^\'\<\{\ \-\"]+[\w\!\@\#\$\%\^\&\*\-\=\+\_\'\<\>\{\}\(\)\[\]\:\;\\\/\|\~\`\ ]+[^\'\>\}\ \-])$"
    _item_name_reg = r"^[^\d]+[\w]+[^\_]{2,}$"
    _password_reg = r"^(?=.*[a-z]{2,})(?=.*[A-Z]{2,})(?=.*[\d]{4,})(?=.*[!@#$%^&*-=+_]{1,})[\w!@#$%^&*-=+]{10,20}$"
    _username_reg = r"^([^\d][\w]{4,12})$"
    _email_reg = r"^([\w\-\.]{2,})+[^\@\.]+[@]+[^\@\.]+[\w\-\.]+[A-Za-z]+[\.][A-Za-z]+$"

    def email_regex(self, email: str) -> bool:
        if self._sanitizer(email):
            return True if re.match(self._email_reg, email) else False

    def username_regex(self, name: str) -> bool:
        if self._sanitizer(name):
            return True if re.match(self._username_reg, name) else False

    def password_regex(self, password: str) -> bool:
        if self._sanitizer(password):
            return True if re.match(self._password_reg, password) else False

    def item_name_regex(self, name: str) -> bool:
        if self._sanitizer(name):
            return True if re.match(self._item_name_reg, name) else False

    def _sanitizer(self, string: str) -> bool:
        return True if re.match(self._sanitizer_reg, string) else False
