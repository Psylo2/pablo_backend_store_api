from typing import TypeVar

T_ITEM = TypeVar("T_ITEM")


def __add_item_to_display(item: T_ITEM, items_result: dict) -> None:
    item_title = item.title

    if item_title not in items_result:
        item_dict = item.to_dict()
        item_dict['ids'] = [item_dict.pop('id')]
        item_dict['quantity'] = 1
        items_result.update({item_title: item_dict})
        return

    items_result[item_title]['ids'].append(item.id)
    items_result[item_title]['quantity'] += 1


def sold_items_display(func):
    def _display_sold(items: list[T_ITEM]) -> list[dict]:
        items_result = {}

        for item in items:
            if not item.sold:
                continue

            __add_item_to_display(item=item, items_result=items_result)

        return list(items_result.values())

    def inner(*args, **kwargs) -> list[dict]:
        items = func(*args, **kwargs)
        return _display_sold(items=items)

    return inner


def items_display(func):
    def _display(items: list[T_ITEM]) -> list[dict]:
        items_result = {}

        for item in items:
            if item.sold:
                continue

            __add_item_to_display(item=item, items_result=items_result)

        return list(items_result.values())

    def inner(*args, **kwargs) -> list[dict]:
        items = func(*args, **kwargs)
        return _display(items=items)

    return inner
