from flask import make_response
from flask_restful import Resource

from application.interfaces.usecases.user.confirmation_interface import ConfirmationInterface
from application.exceptions import UserError

from interface.http.custom_parser import CustomParser


class ConfirmationResource(Resource):
    str_type_name_args = ("email", "confirmation_id")

    def __init__(self, *args, use_case: ConfirmationInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    def get(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_multi_arguments(_type=str, args_names=self.str_type_name_args, required=True, _help=_help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.confirm(confirmation_data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except (Exception, UserError) as err:
            self._use_case.logger.error(f"Error: {err}")
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
