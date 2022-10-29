import os
from datetime import timedelta
from flask import Flask
from logging import Logger

from infrastructure.repositories.orm_adapter import ORMAdapter
from application.interfaces.core.configurations.app_configuration_interface import AppConfigurationInterface
from application.core.logs.console.custom_stream_handler import CustomStreamHandler
from application.core.logs.file.custom_time_rotating_file_handler import CustomTimedRotatingFileHandler


class AppConfigurations(AppConfigurationInterface):
    def __init__(self, app: Flask, repository: ORMAdapter, logger: Logger):
        self._app = app
        self._repository = repository
        self._logger = logger

        self.apply_production_configurations()
        self.configure_file_log()
        self.configure_console_log()

        self.repository_init_app()
        self.repository_create_all_tables()

    @property
    def app(self):
        return self._app

    @property
    def repository(self):
        return self._repository

    @property
    def logger(self):
        return self._logger

    def apply_production_configurations(self) -> None:
        jwt_access_token_minutes = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))
        jwt_refresh_token_minutes = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))

        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('REPOSITORY_URI')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=jwt_access_token_minutes)
        self.app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=jwt_refresh_token_minutes)
        self.app.config['JWT_BLACKLIST_ENABLED'] = True
        self.app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]
        self.app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        self.app.config['APP_SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
        self.app.config['ADMIN'] = os.environ.get('ADMIN')
        self.app.config['GITHUB_CONSUMER_KEY'] = os.environ.get('GITHUB_CONSUMER_KEY')
        self.app.config['GITHUB_CONSUMER_SECRET'] = os.environ.get('GITHUB_CONSUMER_SECRET')
        self.app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')
        self.app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')
        self.app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
        self.app.config['MAX_CONTENT_PATH'] = int(os.environ.get('MAX_CONTENT_PATH'))

    def repository_init_app(self) -> None:
        self.repository.db.init_app(app=self.app)

    def repository_create_all_tables(self) -> None:
        self.repository.db.create_all(app=self.app)

    def configure_file_log(self) -> None:
        folder_name = os.environ.get("LOG_FOLDER_NAME")
        log_handler = CustomTimedRotatingFileHandler(folder_name=folder_name)
        self.logger.addHandler(log_handler)

    def configure_console_log(self) -> None:
        log_handler = CustomStreamHandler()
        self.logger.addHandler(log_handler)

    # def _add_admin(self, user_use_case) -> None:
    #     admin_name = os.environ.get('ADMIN')
    #     if not user_use_case._is_user_name_exist(name=admin_name):
    #         admin = {"id": 1,
    #                  "name": admin_name,
    #                  "email": os.environ.get('ADMIN'),
    #                  "password": os.environ.get('ADMIN')}
    #         user_use_case._user_register(user_data=admin)
