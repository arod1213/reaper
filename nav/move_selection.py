from typing import Literal

import items
import razors
import tracks

direction_type = Literal["up", "down"]


def move_selection(
    count: int = 1, extend: bool = False, direction: direction_type = "up"
) -> None:
    if count < 1:
        raise ValueError("Invalid count")
    track = None
    if direction == "up":
        track = tracks.selection.move_track_selection_up(count=count, extend=extend)
    else:
        track = tracks.selection.move_track_selection_down(count=count, extend=extend)
    if not track:
        return
    start_pos, end_pos, _ = razors.properties.get_bounds()

    if not extend:
        razors.set.clear()
        items.selection.clear()

    track.set_razor(start_pos, end_pos)
