from typing import List

import reaper_python as rp
from models import Track

from . import find


def clear():
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)
    for i in reversed(range(num_sel_tracks)):
        track = Track(rp.RPR_GetSelectedTrack2(0, i, False))
        track.set_selected(False)


def select_tracks(tracks: List[Track], exclusive: bool):
    if exclusive:
        clear()
    for track in tracks:
        track.set_selected(True)


def move_track_selection_up(count: int, extend: bool) -> Track | None:
    first_track = find.get_selected("first")

    track_num = 0
    if first_track and first_track.number != 1:
        track_num = first_track.number - 1 - count

    if not extend:
        clear()

    new_sel_track = Track(rp.RPR_GetTrack(0, track_num))
    new_sel_track.set_selected(True)
    return new_sel_track


def move_track_selection_down(count: int, extend: bool) -> Track | None:
    last_track = find.get_selected("last")
    num_tracks = rp.RPR_CountTracks(0)
    if num_tracks == 0:
        return None

    track_num = num_tracks - 1

    if last_track and last_track.number != num_tracks:
        track_num = last_track.number - 1 + count

    if not extend:
        clear()

    new_sel_track = Track(rp.RPR_GetTrack(0, track_num))
    new_sel_track.set_selected(True)
    return new_sel_track
