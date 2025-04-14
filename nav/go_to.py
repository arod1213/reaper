from typing import Literal

import reaper_python as rp
import tracks
from models import Track
from nav import cursor

location_type = Literal["measure", "track"]


def go_to(location_type: location_type, value: str | int):
    if location_type == "measure":
        if type(value) is not int:
            raise ValueError("Invalid measure input")

        measure = int(value)
        (
            retval,
            proj,
            measure,
            qn_startOut,
            qn_endOut,
            timesig_numOut,
            timesig_denomOut,
            tempoOut,
        ) = rp.RPR_TimeMap_GetMeasureInfo(0, measure, 1, 1, 1, 1, 1)
        qn_adjusted = qn_startOut - ((timesig_numOut / timesig_denomOut) * 4)
        time = rp.RPR_TimeMap_QNToTime(qn_adjusted)
        cursor.set(time)
        return
    elif location_type == "track":
        # console(value)
        if type(value) is int:  # go to track num
            num_tracks = rp.RPR_CountTracks(0)
            if value < 0 or value > num_tracks:
                return  # invalid track num
            int_track = Track(rp.RPR_GetTrack(0, value - 1))
            if not int_track:
                return
            tracks.selection.clear()
            int_track.set_selected(True)
            return
        elif type(value) is str:
            match_track = tracks.find.get_match_by_name(value)
            if match_track:
                tracks.selection.clear()
                match_track.set_selected(True)
