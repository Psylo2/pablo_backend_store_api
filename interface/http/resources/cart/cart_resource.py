from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.interfaces.usecases.cart.cart_interface import CartInterface

class CartResource(Resource):
    def __init__(self, *args, use_case: CartInterface, **kwargs):
        self._use_case = use_case

        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            response, status_code = self._use_case.show_cart(identity=user_id)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def delete(self):
        try:
            user_id = get_jwt_identity()
            response, status_code = self._use_case.remove_cart(identity=user_id)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
