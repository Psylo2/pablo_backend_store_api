from flask_restful import Resource

from application.interfaces.usecases.item.item_interface import ItemInterface
from application.exceptions import PaginationError

from interface.http.custom_parser import CustomParser


class ItemsResource(Resource):
    str_type_name_args = ("platform", "sort_by", "order")

    def __init__(self, *args, use_case: ItemInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    def get(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_multi_arguments(_type=str, args_names=self.str_type_name_args, required=True, _help=_help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.get_items(data=data)
            return response, status_code

        except PaginationError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400


class ItemManufacturerResource(Resource):
    def __init__(self, *args, use_case: ItemInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()

        super().__init__(*args, **kwargs)

        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=str, arg_name="manufacturer", required=True, _help=_help)

    def get(self):
        try:
            parse_data = self._parser.parse_args()
            response, status_code = self._use_case.get_items_manufacturer(data=parse_data)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400


class ItemResource(Resource):
    def __init__(self, *args, use_case: ItemInterface, **kwargs):
        self._use_case = use_case
        self._parser = CustomParser()
        super().__init__(*args, **kwargs)

    def get(self):
        _help = self._use_case.language_manager.get("blank_field_error")
        self._parser.add_single_argument(_type=int, arg_name="id", required=True, _help=_help)

        try:
            data = self._parser.parse_args()
            response, status_code = self._use_case.get_item(data=data)
            return response, status_code

        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
