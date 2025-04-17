import statistics
from typing import Literal

import items
import reaper_python as rp
from models import Track
from nav import cursor
from utils import grid
from view import center

from . import properties


def clear() -> None:
    num_tracks = rp.RPR_CountTracks(0)
    for i in range(num_tracks):
        track = Track(rp.RPR_GetTrack(0, i))
        track.set_razor(None, None)


target_type = Literal["item", "division"]


def extend(
    target_type: target_type = "item",
    direction: grid.direction = "right",
    division: float = 1.0,
) -> None:
    print()
    cursor_pos = float(rp.RPR_GetCursorPosition())

    razor_start, razor_end, _ = properties.get_bounds()

    if direction == "left":
        end_pos = cursor_pos
        if razor_start is not None and razor_end is not None:
            cursor.set(razor_start)
            end_pos = razor_end
        start_pos = None
        match target_type:
            case "item":
                start_pos = items.find.prev_item_position(useBounds=True)
            case "division":
                start_pos = grid.get(cursor_pos, division, direction)
        if start_pos is None:
            return

        set_to_bounds(start_pos, end_pos)
        cursor.set(start_pos, False)
    else:
        start_pos = cursor_pos
        add_from_pos = cursor_pos
        if razor_start is not None and razor_end is not None:
            cursor.set(razor_end, False)
            add_from_pos = razor_end
            start_pos = razor_start
        end_pos = None
        match target_type:
            case "item":
                end_pos = items.find.next_item_position(useBounds=True)
            case "division":
                end_pos = grid.get(add_from_pos, division, direction)
        if not end_pos:
            return

        set_to_bounds(start_pos, end_pos)
        cursor.set(cursor_pos, False)
    rp.RPR_UpdateArrange()


def set_to_bounds(start_pos: float, end_pos: float) -> None:
    num_tracks = rp.RPR_CountTracks(0)
    for i in range(num_tracks):
        track = Track(rp.RPR_GetTrack(0, i))
        if not track.razor.start and not track.selected:
            continue
        track.set_razor(start_pos, end_pos)
    center(
        onValue=statistics.mean([start_pos, end_pos]), minWidth=(end_pos - start_pos)
    )


def set_to_items() -> None:
    start_pos, end_pos = items.find.get_selection_bounds()
    clear()
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)
    for i in range(num_sel_tracks):
        track = Track(rp.RPR_GetSelectedTrack2(0, i, False))
        track.set_razor(start_pos, end_pos)
