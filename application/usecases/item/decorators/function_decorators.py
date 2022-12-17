from typing import TypeVar

T_ITEM = TypeVar("T_ITEM")


def __item_display(item: T_ITEM, items_result: dict[str, any]) -> None:
    item_title = item.title

    if item_title not in items_result:
        item_dict = item.to_dict()
        item_dict['ids'] = [item_dict.pop('id')]
        item_dict['quantity'] = 1
        items_result.update({item_title: item_dict})
        return

    items_result[item_title]['ids'].append(item.id)
    items_result[item_title]['quantity'] += 1

def items_display(include_sold: bool = False) -> callable:
    def decorator(func):
        def _display(items: list[T_ITEM]) -> list[dict[str, any]]:
            items_result = {}

            for item in items:
                if item.sold and not include_sold:
                    continue

                __item_display(item=item, items_result=items_result)

            return list(items_result.values())

        def inner(*args, **kwargs) -> list[dict[str, any]]:
            items = func(*args, **kwargs)
            return _display(items=items)

        return inner
    return decorator
