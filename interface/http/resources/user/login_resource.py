from flask_restful import Resource

from application.interfaces.usecases.user.login_interface import LoginInterface
from application.exceptions import UserError

from interface.http.custom_parser import CustomParser


class LoginResource(Resource):
    str_type_name_args = ("name", "email")

    def __init__(self, *args, use_case: LoginInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_multi_arguments(_type=str, args_names=self.str_type_name_args, required=False, _help=_help)
        self._parser.add_single_argument(_type=str, arg_name='password', required=True, _help=_help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.user_login(user_data=data)
            return response, status_code

        except UserError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
