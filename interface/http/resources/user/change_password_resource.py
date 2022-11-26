from flask import make_response, request
from flask_restful import Resource

from application.interfaces.usecases.user.change_password_interface import ChangePasswordInterface
from application.exceptions import UserError

from interface.http.custom_parser import CustomParser


class ChangePasswordResource(Resource):

    def __init__(self, *args, use_case: ChangePasswordInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

        self._help = self._use_case.language_manager.get("blank_field_error")

    def get(self):
        """Return confirmation HTML page."""
        self._parser.add_multi_arguments(_type=str, args_names=('email', 'confirmation_id'), required=True, _help=self._help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.confirm_email(data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except UserError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    def put(self):
        str_type_name_args = ('confirmation', 'password', 'confirm_password')
        self._parser.add_multi_arguments(_type=str, args_names=str_type_name_args, required=True, _help=self._help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.change_password(data=data)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    def post(self):
        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.send_confirmation_email(data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
