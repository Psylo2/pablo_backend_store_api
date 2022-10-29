from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from application.interfaces.usecases.managment.promo_interface import PromoInterface
from application.exceptions import AdminError

from interface.http.custom_parser import CustomParser

class PromoResource(Resource):
    def __init__(self, *args, use_case: PromoInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()

    @jwt_required
    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name='item_title', required=False, _help=_help)

        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.send_ads(jwt_data=jwt_data, data=parse_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
