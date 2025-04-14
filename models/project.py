from dataclasses import dataclass
from typing import Any, Literal

import reaper_python as rp

from .track import Track

play_states = Literal["playing", "pause", "recording"]


@dataclass
class ArrangeView:
    project: Any
    isSet: bool
    screen_x_start: int
    screen_x_end: int
    start_timeOut: float
    end_timeOut: float


@dataclass
class Markers:
    retval: int
    project: Any
    num_markersOut: int
    num_regionsOut: int


class Project:
    def __init__(self, project):
        self.project = project
        self.name = str(rp.RPR_GetProjectName(project, "", 40)[2])
        self.cursor_pos = float(rp.RPR_GetCursorPositionEx(project))
        self.cursor_context = self.decode_context(rp.RPR_GetCursorContext())

        self.length = rp.RPR_GetProjectLength(project)
        self.saved = bool(rp.RPR_IsProjectDirty(project))
        (hasGridLines, _, _, division, hasSwing, swingAmt) = rp.RPR_GetSetProjectGrid(
            project, False, 0, 0, 0
        )
        self.grid = division
        self.grid_enabled = True if hasGridLines % 2 == 1 else False
        self.swing = swingAmt if hasSwing else 0

        self.markers = Markers(*rp.RPR_CountProjectMarkers(project, 0, 0))
        self.arrange = ArrangeView(
            *rp.RPR_GetSet_ArrangeView2(project, False, 0, 0, 0, 0)
        )

        state = int(rp.RPR_GetAllProjectPlayStates(ignoreProject=-1))
        self.play_state = self.decode_play_state(state)

    def decode_context(self, context: int) -> str:
        match context:
            case 0:
                return "tracks"
            case 1:
                return "items"
            case 2:
                return "envelopes"
        return "tracks"  # fallback

    def set_context(self, focus: Literal["tracks", "items", "envelopes"]):
        context = 0  # default val
        match focus:
            case "tracks":
                context = 0
            case "items":
                context = 1
            case "envelopes":
                context = 2
        rp.RPR_SetCursorContext(context, "")

    def decode_play_state(self, state: int) -> str:
        if state & 4:
            if state & 1:
                return "recording and playing"
            return "recording"
        if state & 1:
            return "playing"
        if state & 2:
            return "paused"
        return "stopped"

    def get_track(self, track_num: int) -> Track:
        num_tracks = rp.RPR_CountTracks(self.project)
        if track_num < 0 or track_num > num_tracks:
            raise ValueError("Invalid track number")
        return Track(rp.RPR_GetTrack(self.project, track_num - 1))
