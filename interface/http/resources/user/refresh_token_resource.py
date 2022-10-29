from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity

from application.interfaces.usecases.user.token_refresh_interface import TokenRefreshInterface

class TokenRefreshResource(Resource):
    def __init__(self, *args, use_case: TokenRefreshInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_refresh_token_required
    def get(self):
        try:
            user_identity = get_jwt_identity()
            response, status_code = self._use_case.refresh_token(identity=user_identity)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
