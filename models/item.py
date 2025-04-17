import reaper_python as rp

from .take import Take
from .track import Track
from typing import Literal


class Item:
    length: float
    start: float
    end: float

    def __init__(self, item):
        self.item = item

        # time properties
        self.length = float(rp.RPR_GetMediaItemInfo_Value(item, "D_LENGTH"))
        self.start = float(rp.RPR_GetMediaItemInfo_Value(item, "D_POSITION"))
        self.end = float(self.start + self.length)

        self.selected = int(rp.RPR_GetMediaItemInfo_Value(item, "B_UISEL"))

        self.track = Track(rp.RPR_GetMediaItem_Track(item))

        self.lanestate = rp.RPR_GetMediaTrackInfo_Value(item, "C_LANESCOLLAPSED")
        self.lanecount = rp.RPR_GetMediaTrackInfo_Value(item, "I_NUMFIXEDLANES")

        self.active_take = Take(rp.RPR_GetActiveTake(item))
        self.fade_in_len = rp.RPR_GetMediaItemInfo_Value(self.item, "D_FADEINLEN")
        self.fade_out_len = rp.RPR_GetMediaItemInfo_Value(self.item, "D_FADEOUTLEN")

    def delete(self):
        rp.RPR_DeleteTrackMediaItem(tr=self.track.track, it=self.item)

    def set_selected(self, value: bool):
        rp.RPR_SetMediaItemInfo_Value(self.item, "B_UISEL", value)

    def loop(self, value: bool):
        rp.RPR_SetMediaItemInfo_Value(self.item, "B_LOOPSRC", value)

    def set_fade(self, fade_type: Literal['in', 'out'], value: float, isAdjust: bool = False, override: bool = False):
        curr_fade = self.fade_in_len
        property = "D_FADEINLEN"
        match (fade_type):
            case ('out'):
                property = "D_FADEOUTLEN"
                curr_fade = self.fade_out_len

        if isAdjust:
            value += curr_fade
        if curr_fade > 0 and not override:
            return
        rp.RPR_SetMediaItemInfo_Value(self.item, property, value)
        rp.RPR_UpdateArrange()


