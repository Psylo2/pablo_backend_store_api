from flask_restful import Resource

from application.interfaces.usecases.user.change_password_interface import ChangePasswordInterface

from interface.http.custom_parser import CustomParser


class ChangePasswordResource(Resource):
    str_type_name_args = ("email", "password")

    def __init__(self, *args, use_case: ChangePasswordInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_multi_arguments(_type=str, args_names=self.str_type_name_args, required=True, _help=_help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.change_password(data=data)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
