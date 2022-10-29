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
from interface.http.resources.item.item_resource import ItemResource, ItemManufacturerResource
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

    def init_api(self, use_cases: dict[str, callable]) -> None:
        self._api.add_resource(RegisterResource, f'{self.API_PREFIX}/register',
                               resource_class_kwargs={"use_case": use_cases['register_use_case']})

        self._api.add_resource(ConfirmationResource, f'{self.API_PREFIX}/confirmation',
                               resource_class_kwargs={"use_case": use_cases['confirmation_use_case']})

        self._api.add_resource(SubscriberResource, f'{self.API_PREFIX}/subscriber',
                               resource_class_kwargs={"use_case": use_cases['subscriber_use_case']})

        # TODO: add confirmation model and logics
        self._api.add_resource(LoginResource, f'{self.API_PREFIX}/login',
                               resource_class_kwargs={"use_case": use_cases['login_use_case']})

        self._api.add_resource(LogoutResource, f'{self.API_PREFIX}/logout',
                               resource_class_kwargs={"use_case": use_cases['logout_use_case']})

        self._api.add_resource(TokenRefreshResource, f'{self.API_PREFIX}/refresh',
                               resource_class_kwargs={"use_case": use_cases['refresh_token_use_case']})

        # TODO
        self._api.add_resource(ChangePasswordResource, f'{self.API_PREFIX}/user/password',
                               resource_class_kwargs={"use_case": use_cases['change_password_use_case']})

        self._api.add_resource(CartResource, f'{self.API_PREFIX}/cart',
                               resource_class_kwargs={"use_case": use_cases['cart_use_case']})

        self._api.add_resource(CartItemsResource, f'{self.API_PREFIX}/cart/<int:item_id>',
                               resource_class_kwargs={"use_case": use_cases['cart_use_case']})

        self._api.add_resource(UserListResource, f'{self.API_PREFIX}/users',
                               resource_class_kwargs={"use_case": use_cases['user_lists_use_case']})

        self._api.add_resource(BlockedUserListResource, f'{self.API_PREFIX}/users/blocked',
                               resource_class_kwargs={"use_case": use_cases['user_lists_use_case']})

        self._api.add_resource(AllowedUserListResource, f'{self.API_PREFIX}/users/allowed',
                               resource_class_kwargs={"use_case": use_cases['user_lists_use_case']})

        self._api.add_resource(ItemResource, f'{self.API_PREFIX}/items',
                               resource_class_kwargs={"use_case": use_cases['item_use_case']})

        self._api.add_resource(ItemManufacturerResource, f'{self.API_PREFIX}/items-manufacture',
                               resource_class_kwargs={"use_case": use_cases['item_use_case']})

        self._api.add_resource(ItemInventoryResource, f'{self.API_PREFIX}/item-inventory',
                               resource_class_kwargs={"use_case": use_cases['item_inventory_use_case']})

        self._api.add_resource(ItemListResource, f'{self.API_PREFIX}/admin-items',
                               resource_class_kwargs={"use_case": use_cases['item_inventory_use_case']})

        self._api.add_resource(SoldItemListResource, f'{self.API_PREFIX}/admin-sold-items',
                               resource_class_kwargs={"use_case": use_cases['item_inventory_use_case']})

        self._api.add_resource(CartListResource, f'{self.API_PREFIX}/carts',
                               resource_class_kwargs={"use_case": use_cases['cart_use_case']})

        self._api.add_resource(PaymentResource, f'{self.API_PREFIX}/payment',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(PaymentRefundResource, f'{self.API_PREFIX}/refund',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(AllPaymentsResource, f'{self.API_PREFIX}/all-payments',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(PaidPaymentsResource, f'{self.API_PREFIX}/paid-payments',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(PendingPaymentsResource, f'{self.API_PREFIX}/pending-payments',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(FailPaymentsResource, f'{self.API_PREFIX}/fail-payments',
                               resource_class_kwargs={"use_case": use_cases['payment_use_case']})

        self._api.add_resource(PromoResource, f'{self.API_PREFIX}/promo',
                               resource_class_kwargs={"use_case": use_cases['promo_use_case']})

        self._api.add_resource(UserBlockResource, f'{self.API_PREFIX}/block',
                               resource_class_kwargs={"use_case": use_cases['user_block_use_case']})

        self._api.add_resource(GithubOauthResource, f'{self.API_PREFIX}/login/github/authorized/thank_you',
                               endpoint="github.authorize",
                               resource_class_kwargs={"use_case": use_cases['github_use_case']})

        self._api.add_resource(GithubLoginApproveResource, f'{self.API_PREFIX}/login/github/authorized"',
                               resource_class_kwargs={"use_case": use_cases['github_use_case']})

        # TODO: [X] manufacturer GET ? maybe use the new endpoint with item pagination instead?
