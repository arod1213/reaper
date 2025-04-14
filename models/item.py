import reaper_python as rp

from .take import Take
from .track import Track


class Item:
    length: float
    start: float
    end: float

    def __init__(self, item):
        self.item = item
        self.length = float(rp.RPR_GetMediaItemInfo_Value(item, "D_LENGTH"))
        self.start = float(rp.RPR_GetMediaItemInfo_Value(item, "D_POSITION"))
        self.end = float(self.start + self.length)
        self.selected = int(rp.RPR_GetMediaItemInfo_Value(item, "B_UISEL"))
        self.track = Track(rp.RPR_GetMediaItem_Track(item))
        self.active_take = Take(rp.RPR_GetActiveTake(item))

    def delete(self):
        rp.RPR_DeleteTrackMediaItem(tr=self.track.track, it=self.item)

    def set_selected(self, value: bool):
        rp.RPR_SetMediaItemInfo_Value(self.item, "B_UISEL", value)
