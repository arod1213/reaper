import reaper_python as rp

from .source import Source


class Take:
    def __init__(self, take):
        self.take = take
        self.volume = float(rp.RPR_GetMediaItemTakeInfo_Value(take, "D_VOL"))
        self.pan = float(rp.RPR_GetMediaItemTakeInfo_Value(take, "D_PAN"))
        self.play_rate = float(rp.RPR_GetMediaItemTakeInfo_Value(take, "D_PLAYRATE"))
        self.pitch = float(rp.RPR_GetMediaItemTakeInfo_Value(take, "D_PITCH"))

        self.source = Source(rp.RPR_GetMediaItemTake_Source(take))
        self.sourcelen = rp.RPR_GetMediaSourceLength(self.source, False)[0]

        self.startoffset = rp.RPR_GetMediaItemTakeInfo_Value(take, "D_STARTOFFS")
        self.playrate = rp.RPR_GetMediaItemTakeInfo_Value(take, "D_PLAYRATE")

        # self.item = Item(rp.RPR_GetMediaItemTakeInfo_Value(take, "P_ITEM"))
        # self.duration = float(self.item.length * self.playrate)
