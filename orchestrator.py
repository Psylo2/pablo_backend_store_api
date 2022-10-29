from flask import Flask
from flask_oauthlib.client import OAuth
from logging import Logger

from application.interfaces.core.managers.language_interface import LanguageInterface
from application.interfaces.core.managers.field_validations_interface import FieldsValidationInterface
from application.interfaces.core.managers.cipher_interface import CaesarCipherInterface

from application.usecases.user.register_usecase import RegisterUseCase
from application.usecases.user.login_usecase import LoginUseCase
from application.usecases.user.logout_usecase import LogoutUseCase
from application.usecases.user.token_refresh_usecase import TokenRefreshUseCase
from application.usecases.user.change_password_usecase import ChangePasswordUseCase
from application.usecases.item.item_usecase import ItemUseCase
from application.usecases.cart.cart_usecase import CartUseCase
from application.usecases.user.user_lists_usecase import UserListsUseCase
from application.usecases.user.confirmation_usecase import ConfirmationUseCase
from application.usecases.user.subscriber_usecase import SubscriberUseCase
from application.usecases.managment.promo.promo_usecase import PromoUseCase
from application.usecases.managment.user_block.user_block_use_case import UserBlockUseCase
from application.usecases.managment.item_inventory.item_inventory_usecase import ItemInventoryUseCase
from application.usecases.managment.password_configuration_usecase import PasswordUseCase
from application.usecases.managment.payment_usecase import PaymentUseCase
from application.usecases.managment.oauths.github_oauth_usecase import GithubOauthUseCase

from infrastructure.repositories.repository_manager import RepositoryManagerInterface

from infrastructure.repositories.queries.user_queries import UserQueries
from infrastructure.repositories.queries.item_queries import ItemQueries
from infrastructure.repositories.queries.cart_queries import CartQueries
from infrastructure.repositories.queries.password_queries import PasswordQueries
from infrastructure.repositories.queries.payment_queries import PaymentQueries
from infrastructure.repositories.queries.confirmation_queries import ConfirmationQueries
from infrastructure.repositories.queries.subscriber_queries import SubscriberQueries

from infrastructure.external_api_services.email_api import EmailAPI, EmailApiInterface
from infrastructure.external_api_services.payments_api import PaymentsAPI, PaymentsApiInterface
from infrastructure.oauth.github_oa import GitHubOAuth, OAuthClientInterface

QueryType = [UserQueries | ItemQueries | CartQueries | PasswordQueries |
             PaymentQueries | ConfirmationQueries | SubscriberQueries]
ApiType = [EmailApiInterface | PaymentsApiInterface]
OauthType = [OAuthClientInterface]

class Orchestrator:
    def __init__(self, app: Flask,
                 repository: RepositoryManagerInterface,
                 logger: Logger,
                 black_list_manager: any,
                 caesar_cipher: CaesarCipherInterface,
                 language_manager: LanguageInterface,
                 field_validator_manager: FieldsValidationInterface):
        self._oauth = OAuth(app=app)
        self._repository = repository
        self._logger = logger
        self._black_list_manager = black_list_manager
        self._caesar_cipher = caesar_cipher
        self._language_manager = language_manager
        self._field_validator_manager = field_validator_manager

        self.oauth_services_mapper = self._create_oauth_services_mapper()
        self.queries_services_mapper = self._create_queries_services_mapper()
        self.external_api_services_mapper = self._create_external_api_service_mapper()

    def _create_queries_services_mapper(self) -> dict[str, QueryType]:
        return {
            "user_queries_service": UserQueries(repository_services=self._repository),
            "item_queries_service": ItemQueries(repository_services=self._repository),
            "cart_queries_service": CartQueries(repository_services=self._repository),
            "password_queries_service": PasswordQueries(repository_services=self._repository),
            "payment_queries_service": PaymentQueries(repository_services=self._repository),
            "confirmation_queries_service": ConfirmationQueries(repository_services=self._repository),
            "subscriber_queries_service": SubscriberQueries(repository_services=self._repository),

        }

    def _create_external_api_service_mapper(self) -> dict[str, ApiType]:
        return {
            "email_api": EmailAPI(language_manager=self._language_manager),
            "payments_api": PaymentsAPI(language_manager=self._language_manager),
        }

    def _create_oauth_services_mapper(self) -> dict[str, OauthType]:
        return {
            "github": GitHubOAuth(oauth=self._oauth),
        }

    def generate_use_cases_mapper(self) -> dict[str, callable]:
        _password_use_case = PasswordUseCase(
            repository_queries=self.queries_services_mapper['password_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            black_list_manager=self._black_list_manager)

        _confirmation_use_case = ConfirmationUseCase(
            repository_queries=self.queries_services_mapper['confirmation_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            caesar_cipher=self._caesar_cipher,
            email_api=self.external_api_services_mapper['email_api'])

        _subscriber_use_case = SubscriberUseCase(
            repository_queries=self.queries_services_mapper['subscriber_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            caesar_cipher=self._caesar_cipher,
            email_api=self.external_api_services_mapper['email_api'])

        _promo_use_case = PromoUseCase(
            repository_queries=self.queries_services_mapper['subscriber_queries_service'],
            item_repository_queries=self.queries_services_mapper['item_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            caesar_cipher=self._caesar_cipher,
            email_api=self.external_api_services_mapper['email_api'])

        _register_use_case = RegisterUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            confirmation_use_case=_confirmation_use_case,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            caesar_cipher=self._caesar_cipher)

        _login_use_case = LoginUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            confirmation_use_case=_confirmation_use_case,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            caesar_cipher=self._caesar_cipher)

        _change_password_use_case = ChangePasswordUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            password_use_case=_password_use_case,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _logout_use_case = LogoutUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            black_list_manager=self._black_list_manager)

        _refresh_token_use_case = TokenRefreshUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager)

        _item_use_case = ItemUseCase(
            repository_queries=self.queries_services_mapper['item_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _item_inventory_use_case = ItemInventoryUseCase(
            repository_queries=self.queries_services_mapper['item_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _cart_use_case = CartUseCase(
            repository_queries=self.queries_services_mapper['cart_queries_service'],
            item_repository_queries=self.queries_services_mapper['item_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _payment_use_case = PaymentUseCase(
            repository_queries=self.queries_services_mapper['payment_queries_service'],
            cart_repository_queries=self.queries_services_mapper['cart_queries_service'],
            item_repository_queries=self.queries_services_mapper['item_queries_service'],
            user_repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager,
            black_list_manager=self._black_list_manager,
            caesar_cipher=self._caesar_cipher,
            payments_api=self.external_api_services_mapper['payments_api'])

        _user_lists_use_case = UserListsUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _user_block_use_case = UserBlockUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            field_validation_manager=self._field_validator_manager)

        _github_use_case = GithubOauthUseCase(
            repository_queries=self.queries_services_mapper['user_queries_service'],
            logger=self._logger,
            language_manager=self._language_manager,
            black_list_manager=self._black_list_manager,
            password_service=_password_use_case,
            github_service=self.oauth_services_mapper['github'])

        return {
            "register_use_case": _register_use_case,
            "confirmation_use_case": _confirmation_use_case,
            "subscriber_use_case": _subscriber_use_case,
            "promo_use_case": _promo_use_case,
            "user_block_use_case": _user_block_use_case,
            "login_use_case": _login_use_case,
            "logout_use_case": _logout_use_case,
            "refresh_token_use_case": _refresh_token_use_case,
            "change_password_use_case": _change_password_use_case,
            "cart_use_case": _cart_use_case,
            "user_lists_use_case": _user_lists_use_case,
            "item_use_case": _item_use_case,
            "item_inventory_use_case": _item_inventory_use_case,
            "payment_use_case": _payment_use_case,
            "github_use_case": _github_use_case,
        }
