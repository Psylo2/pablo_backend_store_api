from flask_restful import Resource
from flask_jwt_extended import get_jwt_claims

from application.interfaces.usecases.managment.payment_interface import PaymentInterface
from application.exceptions import AdminError

class AllPaymentsResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.all_payments(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

class PaidPaymentsResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.paid_payments(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

class PendingPaymentsResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.pending_payments(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

class FailPaymentsResource(Resource):
    def __init__(self, *args, use_case: PaymentInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.fail_payments(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
