from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from interface.http.resources.user.register_resource import RegisterResource
from interface.http.resources.user.login_resource import LoginResource
from interface.http.resources.user.logout_resource import LogoutResource
from interface.http.resources.user.refresh_token_resource import TokenRefreshResource
from interface.http.resources.user.change_password_resource import ChangePasswordResource
from interface.http.resources.user.confirmation_resource import ConfirmationResource
from interface.http.resources.user.subscriber_resource import SubscriberResource
from interface.http.resources.cart.cart_resource import CartResource
from interface.http.resources.cart.cart_items_resource import CartItemsResource
from interface.http.resources.item.item_resource import ItemResource, ItemManufacturerResource, ItemsResource
from interface.http.resources.managment.promo.promo_resource import PromoResource
from interface.http.resources.managment.user_block.user_block_resource import UserBlockResource
from interface.http.resources.user.user_list_resource import UserListResource
from interface.http.resources.item.item_list_resource import ItemListResource, SoldItemListResource
from interface.http.resources.cart.cart_list_resource import CartListResource
from interface.http.resources.managment.payment.payment_resource import PaymentResource, PaymentRefundResource
from interface.http.resources.managment.payment.payment_list_resource import (AllPaymentsResource,
                                                                              PaidPaymentsResource,
                                                                              PendingPaymentsResource,
                                                                              FailPaymentsResource)
from interface.http.resources.managment.user_block.blocked_user_list_resource import BlockedUserListResource
from interface.http.resources.managment.user_block.allowed_user_list_resource import AllowedUserListResource
from interface.http.resources.managment.item_inventory.item_inventory_resource import ItemInventoryResource
from interface.http.resources.managment.oauths.github_oauth_resource import GithubOauthResource
from interface.http.resources.managment.oauths.github_login_approve_resource import GithubLoginApproveResource

from application.core.configurations.jwt_manager_configurations import JWTConfigurationManager


class HttpAdapter:
    API_PREFIX = "/api/v1"

    def __init__(self, app: Flask, black_list_manager: any) -> None:
        JWTConfigurationManager(app=app, black_list_manager=black_list_manager)
        CORS(app=app, resources=fr'{self.API_PREFIX}/*')
        self._api = Api(app=app)

    def init_http_adapter(self, use_cases: dict[str, callable]) -> None:
        self._register_html_base_route()
        self._register_html_error_route()
        self._register_api_resources(use_cases=use_cases)

    def _register_html_base_route(self) -> None:
        @self._api.app.route('/')
        def index():
            return self._api.app.send_static_file('index.html')

    def _register_html_error_route(self) -> None:
        @self._api.app.errorhandler(404)
        def not_found(e):
            return self._api.app.send_static_file('index.html')

    def _register_api_resources(self, use_cases: dict[str, callable]) -> None:
        resources = self._generate_resources(use_cases=use_cases)

        for resource in resources:
            self._api.add_resource(
                resource.get('resource'),
                f"{self.API_PREFIX}/{resource.get('url_path')}",
                endpoint=resource.get('endpoint'),
                resource_class_kwargs={"use_case": resource.get('use_case')},

            )

    @staticmethod
    def _generate_resources(use_cases: dict[str, callable]) -> list[dict]:
        return [
            {"resource": RegisterResource,
             "url_path": "register",
             "use_case": use_cases["register_use_case"]
             },
            {
                "resource": ConfirmationResource,
                "url_path": "confirmation",
                "use_case": use_cases["confirmation_use_case"]
            },
            {
                "resource": SubscriberResource,
                "url_path": "subscriber",
                "use_case": use_cases["subscriber_use_case"]
            },
            {
                "resource": LoginResource,
                "url_path": "login",
                "use_case": use_cases["login_use_case"]
            },
            {
                "resource": LogoutResource,
                "url_path": "logout",
                "use_case": use_cases["logout_use_case"]
            },
            {
                "resource": TokenRefreshResource,
                "url_path": "refresh",
                "use_case": use_cases["refresh_token_use_case"]
            },
            {
                "resource": ChangePasswordResource,
                "url_path": "change-password",
                "use_case": use_cases["change_password_use_case"]
            },
            {
                "resource": CartResource,
                "url_path": "cart",
                "use_case": use_cases["cart_use_case"]
            },
            {
                "resource": CartItemsResource,
                "url_path": "cart/item",
                "use_case": use_cases["cart_use_case"]
            },
            {
                "resource": UserListResource,
                "url_path": "users",
                "use_case": use_cases["user_lists_use_case"]
            },
            {
                "resource": BlockedUserListResource,
                "url_path": "users/blocked",
                "use_case": use_cases["user_lists_use_case"]
            },
            {
                "resource": AllowedUserListResource,
                "url_path": "users/allowed",
                "use_case": use_cases["user_lists_use_case"]
            },
            {
                "resource": ItemsResource,
                "url_path": "items",
                "use_case": use_cases["item_use_case"]
            },
            {
                "resource": ItemResource,
                "url_path": "item",
                "use_case": use_cases["item_use_case"]
            },
            {
                "resource": ItemManufacturerResource,
                "url_path": "items-manufacture",
                "use_case": use_cases["item_use_case"]
            },
            {
                "resource": ItemInventoryResource,
                "url_path": "item-inventory",
                "use_case": use_cases["item_inventory_use_case"]
            },
            {
                "resource": ItemListResource,
                "url_path": "admin-items",
                "use_case": use_cases["item_inventory_use_case"]
            },
            {
                "resource": SoldItemListResource,
                "url_path": "admin-sold-items",
                "use_case": use_cases["item_inventory_use_case"]
            },
            {
                "resource": CartListResource,
                "url_path": "carts",
                "use_case": use_cases["cart_use_case"]
            },
            {
                "resource": PaymentResource,
                "url_path": "payment",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": PaymentRefundResource,
                "url_path": "refund",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": AllPaymentsResource,
                "url_path": "all-payments",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": PaidPaymentsResource,
                "url_path": "paid-payments",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": PendingPaymentsResource,
                "url_path": "pending-payments",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": FailPaymentsResource,
                "url_path": "fail-payments",
                "use_case": use_cases["payment_use_case"]
            },
            {
                "resource": PromoResource,
                "url_path": "promo",
                "use_case": use_cases["promo_use_case"]
            },
            {
                "resource": UserBlockResource,
                "url_path": "block",
                "use_case": use_cases["user_block_use_case"]
            },
            {
                "resource": GithubOauthResource,
                "url_path": "login/github/authorized/thank_you",
                "endpoint": "github.authorize",
                "use_case": use_cases["github_use_case"]
            },
            {
                "resource": GithubLoginApproveResource,
                "url_path": "login/github/authorized",
                "use_case": use_cases["github_use_case"]
            },
        ]
