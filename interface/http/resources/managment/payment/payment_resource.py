from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from application.interfaces.usecases.managment.payment_interface import PaymentInterface
from application.exceptions import UserError, CartError, PaymentError

from interface.http.custom_parser import CustomParser


class PaymentResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name="token", required=True, _help=_help)

        try:
            user_id = get_jwt_identity()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.payment(identity=user_id, data=parse_data)
            return response, status_code

        except (UserError, CartError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            response, status_code = self._use_case.get_user_payments(identity=user_id)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400


class PaymentRefundResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name="transaction_id", required=True, _help=_help)

        try:
            user_id = get_jwt_identity()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.full_refund(identity=user_id, data=parse_data)
            return response, status_code

        except (UserError, PaymentError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    # @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            response, status_code = self._use_case.get_user_refund(identity=user_id)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
