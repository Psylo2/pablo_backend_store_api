from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from application.interfaces.usecases.managment.item_inventory_interface import ItemInventoryInterface
from application.exceptions import AdminError, ItemError

from interface.http.custom_parser import CustomParser


class ItemInventoryResource(Resource):
    str_type_name_args = ("title", "manufacturer")
    bool_type_name_args = ("on_sale", "on_stock")
    int_type_name_args = ("engine_hs_power", "original_price", "discount")

    def __init__(self, *args, use_case: ItemInventoryInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    @jwt_required
    def post(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_multi_arguments(_type=str, args_names=self.str_type_name_args, required=True, _help=_help)
        self._parser.add_multi_arguments(_type=bool, args_names=self.bool_type_name_args, required=True, _help=_help)
        self._parser.add_multi_arguments(_type=int, args_names=self.int_type_name_args, required=True, _help=_help)
        self._parser.add_single_argument(_type=int, arg_name="quantity", required=True, _help=_help)

        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            file = request.files.get('file')
            response, status_code = self._use_case.create_item(jwt_data=jwt_data, data=parse_data, file=file)
            return response, status_code

        except (AdminError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def patch(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name="title", required=True, _help=_help)
        self._parser.add_single_argument(_type=str, arg_name="manufacturer", required=False, _help=_help)
        self._parser.add_multi_arguments(_type=bool, args_names=self.bool_type_name_args, required=False, _help=_help)
        self._parser.add_multi_arguments(_type=int, args_names=self.int_type_name_args, required=False, _help=_help)

        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            file = request.files.get('file')
            response, status_code = self._use_case.update_item(jwt_data=jwt_data, data=parse_data, file=file)
            return response, status_code

        except (AdminError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def delete(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name="title", required=True, _help=_help)

        try:
            # jwt_data = get_jwt_claims()
            jwt_data = {}
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.remove_item(jwt_data=jwt_data, data=parse_data)
            return response, status_code

        except (AdminError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

    @jwt_required
    def get(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=int, arg_name="id", required=True, _help=_help)
        self._parser.add_single_argument(_type=str, arg_name="name", required=True, _help=_help)

        try:
            jwt_data = get_jwt_claims()
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.show_item(jwt_data=jwt_data, data=parse_data)
            return response, status_code

        except (AdminError, ItemError) as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
