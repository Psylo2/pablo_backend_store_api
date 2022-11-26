from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.interfaces.usecases.cart.cart_interface import CartInterface
from application.exceptions import CartError, ItemError

from interface.http.custom_parser import CustomParser


class CartItemsResource(Resource):

    def __init__(self, *args, use_case: CartInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=int, arg_name="item_id", required=True, _help=_help)

    @jwt_required
    def post(self):
        try:
            data = self._parser.parse_args()
            data["user_id"] = get_jwt_identity()

            response, status_code = self._use_case.add_item(data=data)
            return response, status_code

        except CartError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except ItemError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 402
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def delete(self):
        try:
            data = self._parser.parse_args()
            data["user_id"] = get_jwt_identity()

            response, status_code = self._use_case.remove_item(data=data)
            return response, status_code

        except CartError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except ItemError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 402
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
