import reaper_python as rp
from models import Item

from . import properties
import tracks


def clear() -> None:
    num_sel_items = rp.RPR_CountSelectedMediaItems(0)
    for i in reversed(range(num_sel_items)):
        item = Item(rp.RPR_GetSelectedMediaItem(0, i))
        item.set_selected(False)


def select_items_in_bounds(start_pos: float, end_pos: float):
    if start_pos >= end_pos:
        raise ValueError("Invalid input: positions cant overlap")
    avail_tracks = tracks.find.selected_or_editable()
    rp.RPR_ShowConsoleMsg(len(avail_tracks))
    for track in avail_tracks:
        num_items = rp.RPR_CountTrackMediaItems(track.track)
        for a in range(num_items):
            item = Item(rp.RPR_GetTrackMediaItem(track.track, a))
            if properties.is_item_in_bounds(item, start_pos, end_pos):
                item.set_selected(True)


def get_selected_items_bounds() -> tuple[float | None, float | None]:
    num_sel_items = rp.RPR_CountSelectedMediaItems(0)
    min_pos, max_pos = None, None
    for i in range(num_sel_items):
        item = Item(rp.RPR_GetSelectedMediaItem(0, i))
        if min_pos is None or item.start < min_pos:
            min_pos = item.start
        if max_pos is None or item.start > max_pos:
            max_pos = item.end
    return min_pos, max_pos
