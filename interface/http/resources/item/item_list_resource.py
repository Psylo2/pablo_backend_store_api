from flask_restful import Resource
from flask_jwt_extended import get_jwt_claims

from application.interfaces.usecases.managment.item_inventory_interface import ItemInventoryInterface
from application.exceptions import AdminError

class ItemListResource(Resource):
    def __init__(self, *args, use_case: ItemInventoryInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.items_list(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400

class SoldItemListResource(Resource):
    def __init__(self, *args, use_case: ItemInventoryInterface, **kwargs):
        self._use_case = use_case
        super().__init__(*args, **kwargs)

    # @jwt_required
    def get(self):
        try:
            jwt_data = get_jwt_claims()
            response, status_code = self._use_case.sold_items_list(jwt_data=jwt_data)
            return response, status_code

        except AdminError as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 401
        except Exception as err:
            return {"message": self._use_case.language_manager.get("error_occurred"),
                    "details": str(err)}, 400
