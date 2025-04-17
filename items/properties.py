from models import Item
import reaper_python as rp


def is_item_in_bounds(item: Item, start_pos: float, end_pos: float):
    if item.start >= end_pos or item.end <= start_pos:
        return False
    return True


def set_fades():
    num_sel_items = rp.RPR_CountSelectedMediaItems(0)
    for i in range(num_sel_items):
        item = Item(rp.RPR_GetSelectedMediaItem(0, i))
        item.set_fade("in", 0.03)
        item.set_fade("out", 0.03)
