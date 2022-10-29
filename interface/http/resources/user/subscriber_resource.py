from flask import make_response
from flask_restful import Resource

from application.interfaces.usecases.user.subscriber_interface import SubscriberInterface
from application.exceptions import UserError

from interface.http.custom_parser import CustomParser


class SubscriberResource(Resource):
    def __init__(self, *args, use_case: SubscriberInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

        self._help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name='email', required=True, _help=self._help)

    def get(self):
        """Return confirmation HTML page."""
        self._parser.add_single_argument(_type=str, arg_name='confirmation_id', required=True, _help=self._help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.confirm_subscriber(data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except UserError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    def post(self):

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.add_subscriber(data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    def delete(self):

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.remove_subscriber(data=data)

            if status_code:
                return response, status_code
            return make_response(response, 200)

        except UserError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
