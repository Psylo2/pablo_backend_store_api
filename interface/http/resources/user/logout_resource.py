from flask_restful import Resource
from flask_jwt_extended import get_raw_jwt

from application.interfaces.usecases.user.logout_interface import LogoutInterface

class LogoutResource(Resource):
    def __init__(self, *args, use_case: LogoutInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def post(self):
        try:
            data = get_raw_jwt()
            response, status_code = self._use_case.user_logout(data=data)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
