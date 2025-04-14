from dataclasses import dataclass
from typing import Literal, Optional

import reaper_python as rp
from models import Item, Track
from models.project import Project
from utils import compare


def get(track_num: int):
    if track_num < 1:
        raise ValueError("Invalid track num")
    return Track(rp.RPR_GetTrack(0, track_num - 1))


@dataclass
class MatchResult:
    track: Optional[Track]
    score: float


def get_match_by_name(name: str) -> Track | None:
    num_tracks = rp.RPR_CountTracks(0)
    best_match = MatchResult(track=None, score=0.0)
    for i in range(num_tracks):
        track = Track(rp.RPR_GetTrack(0, i))
        score = compare.similar(track.name, name)
        if score > best_match.score:
            best_match.track = track
            best_match.score = score
    return best_match.track


def get_match(value: str | int) -> Track | None:
    """Retrieve track matching either name or int

    Args:
        value (str | int): Either track number or track name

    Returns:
        Track | None: returns the matching track
    """

    if type(value) is str:
        return get_match_by_name(value)
    else:
        return Project(0).get_track(int(value))


position = Literal["first", "last"]


def get_selected(position: position = "first") -> Track | None:
    track_num = 0
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)
    if num_sel_tracks > 0:
        if position == "last":
            track_num = num_sel_tracks - 1
        return Track(rp.RPR_GetSelectedTrack2(0, track_num, False))

    # fallback to razor
    num_tracks = rp.RPR_CountTracks(0)
    for i in range(num_tracks):
        track = Track(rp.RPR_GetTrack(0, i))
        if track.razor.start is not None or track.razor.end is not None:
            return track

    # fallback to sel items
    num_sel_items = rp.RPR_CountSelectedMediaItems(0)
    if num_sel_items == 0:
        return None
    item = Item(rp.RPR_GetSelectedMediaItem(0, 0))
    return item.track
