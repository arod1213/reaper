from models import Item


def is_item_in_bounds(item: Item, start_pos: float, end_pos: float):
    if item.start >= end_pos or item.end <= start_pos:
        return False
    return True
