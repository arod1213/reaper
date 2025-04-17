from typing import Literal

import items
import razors
import reaper_python as rp
from models import Project
from nav import cursor
from utils import grid
from view import center


def get() -> float:
    return float(rp.RPR_GetCursorPosition())


def set(time: float, isCenter: bool = False) -> None:
    rp.RPR_SetEditCurPos(time, True, False)
    if isCenter:
        center(time)


def move(time_adjust: float, isCenter: bool = False) -> None:
    cursor_pos = Project(0).cursor_pos
    rp.RPR_MoveEditCursor(time_adjust, False)
    if isCenter:
        center(cursor_pos + time_adjust)


direction = Literal["prev", "next"]


def move_to_item(direction: direction = "next", useBounds: bool = False) -> None:
    razors.set.clear()

    pos = None
    if direction == "prev":
        pos = items.find.prev_item_position(useBounds)
    elif direction == "next":
        pos = items.find.next_item_position(useBounds)

    if pos is None:
        return
    set(pos, False)


def move_by_screen(direction: Literal["left", "right"]):
    project = Project(0)
    view_length = project.arrange.end_timeOut - project.arrange.start_timeOut
    amount = view_length / 50 * (-1 if direction == "left" else 1)

    cursor_position = get()
    time = cursor_position + amount

    razor_start, razor_end, _ = razors.properties.get_bounds()

    if razor_start is not None and cursor_position != razor_start:
        cursor.move(razor_start - cursor_position)
        return

    # update length to be grid based as param
    if type(razor_start) is float and type(razor_end) is float:
        razor_length = razor_end - razor_start
        razor_start = time
        razor_end = time + razor_length
        razors.set.set_to_bounds(razor_start, razor_end)

    set(time)


def move_to_division(division: float, direction: grid.direction = "right") -> None:
    cursor_position = get()
    time = grid.get(cursor_position, division, direction)

    razor_start, razor_end, _ = razors.properties.get_bounds()

    if razor_start is not None and cursor_position != razor_start:
        cursor.move(razor_start - cursor_position)
        return

    # update length to be grid based as param
    if type(razor_start) is float and type(razor_end) is float:
        razor_length = razor_end - razor_start
        razor_start = time
        razor_end = time + razor_length
        razors.set.set_to_bounds(razor_start, razor_end)

    set(time)
