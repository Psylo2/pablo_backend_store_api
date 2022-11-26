from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from application.interfaces.usecases.user.user_lists_interface import UserListsInterface
from application.exceptions import AdminError

class AllowedUserListResource(Resource):
    def __init__(self, *args, use_case: UserListsInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.allowed_users_list(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
