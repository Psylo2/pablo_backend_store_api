from flask_restful import Resource

from application.interfaces.usecases.managment.oauth_interface import OAuthInterface

class GithubOauthResource(Resource):
    def __init__(self, *args, use_case: OAuthInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    def get(self):
        try:
            response, status_code = self._use_case.user_authorize()
            return response, status_code
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
