import reaper_python as rp
from utils.gain import amp_to_db, db_to_amp

from .razor import Razor


class Track:
    def __init__(self, track):
        self.track = track
        self.number = int(rp.RPR_GetMediaTrackInfo_Value(track, "IP_TRACKNUMBER"))
        self.selected = int(rp.RPR_GetMediaTrackInfo_Value(track, "I_SELECTED"))
        self.volume = float(rp.RPR_GetMediaTrackInfo_Value(track, "D_VOL"))
        self.pan = float(rp.RPR_GetMediaTrackInfo_Value(track, "D_PAN"))
        self.width = float(rp.RPR_GetMediaTrackInfo_Value(track, "D_WIDTH"))
        self.name = rp.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", "", False)[3]
        self.razor = Razor(track)
        self.fx_enabled = rp.RPR_GetMediaTrackInfo_Value(self.track, "I_FXEN")

    def delete(self):
        rp.RPR_DeleteTrack(self.track)

    def set_mute(self, value: bool):
        rp.RPR_SetMediaTrackInfo_Value(self.track, "B_MUTE", value)

    def set_solo(self, value: bool):
        rp.RPR_SetMediaTrackInfo_Value(self.track, "I_SOLO", 1 if value else 0)

    def set_gain(self, db: float, isAdjust: bool = False):
        if isAdjust:
            db += amp_to_db(self.volume)
        amp = db_to_amp(db)
        rp.RPR_SetMediaTrackInfo_Value(self.track, "D_VOL", amp)

    def set_pan(self, position: float, isAdjust: bool = False):
        if isAdjust:
            position += self.pan
        rp.RPR_SetMediaTrackInfo_Value(self.track, "D_PAN", position)

    def set_fx_enabled(self, value: bool):
        rp.RPR_SetMediaTrackInfo_Value(self.track, "I_FXEN", 1 if value else 0)

    def set_selected(self, value: bool):
        rp.RPR_SetMediaTrackInfo_Value(self.track, "I_SELECTED", 1 if value else 0)

    def set_razor(self, start_pos: float | None, end_pos: float | None):
        bounds = f"{start_pos} {end_pos}"
        # if (start_pos is None or end_pos is None):
        #     bounds = " " # force bounds to be empty
        rp.RPR_GetSetMediaTrackInfo_String(self.track, "P_RAZOREDITS", bounds, True)
