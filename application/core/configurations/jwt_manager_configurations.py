from flask import Flask
from flask_jwt_extended import JWTManager


class JWTConfigurationManager:
    def __init__(self, app: Flask, black_list_manager: set):
        jwt = JWTManager(app=app)

        @jwt.token_in_blacklist_loader
        def check_if_token_in_blacklist(decrypted_token) -> bool:
            return decrypted_token["jti"] in black_list_manager

        @jwt.user_claims_loader
        def add_claims_to_jwt(identity) -> dict:
            if identity == 1:
                return {'is_admin': True}
            return {'is_admin': False}
