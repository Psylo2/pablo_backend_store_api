from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from application.interfaces.usecases.managment.user_block_interface import UserBlockInterface
from application.exceptions import AdminError, UserError

from interface.http.custom_parser import CustomParser


class UserBlockResource(Resource):
    def __init__(self, *args, use_case: UserBlockInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

        self._help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name='user_id', required=False, _help=self._help)

    @jwt_required
    def post(self):
        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.block_user(jwt_data=jwt_data, data=parse_data)
            return response, status_code

        except (AdminError, UserError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def delete(self):
        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.unblock_user(jwt_data=jwt_data, data=parse_data)
            return response, status_code

        except (AdminError, UserError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
