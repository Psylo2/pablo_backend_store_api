from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.interfaces.usecases.cart.cart_interface import CartInterface
from application.exceptions import CartError, ItemError

class CartItemsResource(Resource):
    def __init__(self, *args, use_case: CartInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self, item_id: int):
        try:
            data = {"user_id": get_jwt_identity(),
                    "item_id": item_id}

            response, status_code = self._use_case.add_item(data=data)
            return response, status_code

        except (CartError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def delete(self, item_id: int):
        try:
            data = {"user_id": get_jwt_identity(),
                    "item_id": item_id}

            response, status_code = self._use_case.remove_item(data=data)
            return response, status_code

        except (CartError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
