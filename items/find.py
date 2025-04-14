import reaper_python as rp
from models import Item, Project, Track
from utils import compare


def get_selection_bounds() -> tuple[float | None, float | None]:
    num_sel_items = rp.RPR_CountSelectedMediaItems(0)
    start_pos, end_pos = None, None
    for i in range(num_sel_items):
        item = Item(rp.RPR_GetSelectedMediaItem(0, i))
        if start_pos is None or compare.less_than(item.start, start_pos):
            start_pos = item.start
        if end_pos is None or compare.greater_than(item.end, end_pos):
            end_pos = item.end
    return start_pos, end_pos


def next_item_position(useBounds: bool = False) -> float | None:
    cursor = Project(0).cursor_pos
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)

    min_pos = None
    for i in range(num_sel_tracks):
        track_min = None
        track = Track(rp.RPR_GetSelectedTrack2(0, i, False))
        num_items = rp.RPR_CountTrackMediaItems(track.track)
        for a in reversed(range(num_items)):
            item = Item(rp.RPR_GetTrackMediaItem(track.track, a))
            if useBounds and compare.greater_than(item.end, cursor):
                track_min = item.end
            if compare.greater_than(item.start, cursor):
                track_min = item.start
        if track_min and (min_pos is None or compare.less_than(track_min, min_pos)):
            min_pos = track_min

    if min_pos is None:
        return None
    return min_pos


def prev_item_position(useBounds: bool = False) -> float | None:
    cursor = Project(0).cursor_pos
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)

    max_pos = None
    for i in range(num_sel_tracks):
        track_max = None
        track = Track(rp.RPR_GetSelectedTrack2(0, i, False))
        num_items = rp.RPR_CountTrackMediaItems(track.track)
        for a in range(num_items):
            item = Item(rp.RPR_GetTrackMediaItem(track.track, a))
            if compare.less_than(item.start, cursor):
                track_max = item.start
            if useBounds and compare.less_than(item.end, cursor):
                track_max = item.end
        if track_max is None:
            continue
        if max_pos is None or compare.greater_than(track_max, max_pos):
            max_pos = track_max

    if max_pos is None:
        return None
    return max_pos
