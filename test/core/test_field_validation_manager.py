from unittest import TestCase

from application.core.managers.field_validation_manager import FieldsValidationManager

class TestFieldValidation(TestCase):

    def setUp(self) -> None:
        self.field_validation_manager = FieldsValidationManager()

    def test_email_regex(self) -> None:
        invalid_email = "S@op.co.il"
        email_regex_result = self.field_validation_manager.email_regex(email=invalid_email)
        self.assertFalse(expr=email_regex_result, msg="Invalid email")

        invalid_email = "sadasdas.@op.co.il"
        email_regex_result = self.field_validation_manager.email_regex(email=invalid_email)
        self.assertFalse(expr=email_regex_result, msg="Invalid email")

        invalid_email = "sadasdas@.op.co.il"
        email_regex_result = self.field_validation_manager.email_regex(email=invalid_email)
        self.assertFalse(expr=email_regex_result, msg="Invalid email")

        invalid_email = "sadasdas@.op.co.il"
        email_regex_result = self.field_validation_manager.email_regex(email=invalid_email)
        self.assertFalse(expr=email_regex_result, msg="Invalid email")

        invalid_email = "Shoppa@op.co.il"
        email_regex_result = self.field_validation_manager.email_regex(email=invalid_email)
        self.assertTrue(expr=email_regex_result, msg="Valid email")

    def test_username_regex(self) -> None:
        invalid_username = "4Shopper"
        username_regex_result = self.field_validation_manager.username_regex(name=invalid_username)
        self.assertFalse(expr=username_regex_result, msg="Invalid username")

        invalid_username = "!#Shopper"
        username_regex_result = self.field_validation_manager.username_regex(name=invalid_username)
        self.assertFalse(expr=username_regex_result, msg="Invalid username")

        invalid_username = "Shopper4"
        username_regex_result = self.field_validation_manager.username_regex(name=invalid_username)
        self.assertTrue(expr=username_regex_result, msg="Valid username")

    def test_password_regex(self) -> None:
        invalid_password = "a123456789Q!@"
        password_regex_result = self.field_validation_manager.password_regex(password=invalid_password)
        self.assertFalse(expr=password_regex_result, msg="Invalid item_name")

        invalid_password = "aaA1234567890!@#@"
        password_regex_result = self.field_validation_manager.password_regex(password=invalid_password)
        self.assertFalse(expr=password_regex_result, msg="Invalid password")

        invalid_password = "aaAA1345!"
        password_regex_result = self.field_validation_manager.password_regex(password=invalid_password)
        self.assertFalse(expr=password_regex_result, msg="Invalid password")

        invalid_password = "aaAA12345678!@"
        password_regex_result = self.field_validation_manager.password_regex(password=invalid_password)
        self.assertTrue(expr=password_regex_result, msg="Valid password")

    def test_item_name_regex(self) -> None:
        invalid_item_name = "5Itemname"
        item_name_regex_result = self.field_validation_manager.item_name_regex(name=invalid_item_name)
        self.assertFalse(expr=item_name_regex_result, msg="Invalid item_name")

        invalid_item_name = "Itemname_"
        item_name_regex_result = self.field_validation_manager.item_name_regex(name=invalid_item_name)
        self.assertFalse(expr=item_name_regex_result, msg="Invalid item_name")

        invalid_item_name = "Item-name4"
        item_name_regex_result = self.field_validation_manager.item_name_regex(name=invalid_item_name)
        self.assertTrue(expr=item_name_regex_result, msg="Valid item_name")

    def test_sanitizer(self) -> None:
        sql_injection = "' UNION SELECT username, password FROM users--"
        sanitizer_regex_result = self.field_validation_manager._sanitizer(string=sql_injection)
        self.assertFalse(expr=sanitizer_regex_result, msg="Invalid password")

        sql_injection = "SELECT * FROM products WHERE category = 'Gifts'--'"
        sanitizer_regex_result = self.field_validation_manager._sanitizer(string=sql_injection)
        self.assertFalse(expr=sanitizer_regex_result, msg="Invalid password")

        sql_injection = "SELECT * FROM USER WHERE USERID = '" + "234" +"'"
        sanitizer_regex_result = self.field_validation_manager._sanitizer(string=sql_injection)
        self.assertFalse(expr=sanitizer_regex_result, msg="Invalid password")
