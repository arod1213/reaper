import reaper_python as rp


class MediaItem:

    def __init__(self, item):
        self.id = item
        self.length = rp.RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
        self.take = rp.RPR_GetMediaItemTake(
            self.id, int(rp.RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE"))
        )
        self.playrate = rp.RPR_GetMediaItemTakeInfo_Value(self.take, "D_PLAYRATE")
        self.filelength = float(self.length * self.playrate)
        self.isloop = rp.RPR_GetMediaItemInfo_Value(self.id, "B_LOOPSRC")
        self.source = rp.RPR_GetMediaItemTake_Source(self.take)
        self.sourcelen = rp.RPR_GetMediaSourceLength(self.source, False)[0]
        self.startoffset = rp.RPR_GetMediaItemTakeInfo_Value(self.take, "D_STARTOFFS")

    def loop(self, bool):
        if bool:
            bool = 1
        else:
            bool = 0
        rp.RPR_SetMediaItemInfo_Value(self.id, "B_LOOPSRC", bool)

    def exceedsFile(self):
        if self.filelength + self.startoffset > self.sourcelen:
            return True
        else:
            return False

    def trimToFileBounds(self):
        # console(self.sourcelen)
        # console(self.startoffset)
        x = (self.sourcelen - self.startoffset) / self.playrate
        rp.RPR_SetMediaItemInfo_Value(self.id, "D_LENGTH", x)


def loopOff():
    # console(rp.RPR_CountSelectedMediaItems(0))
    for x in range(0, rp.RPR_CountSelectedMediaItems(0)):
        item = MediaItem(rp.RPR_GetSelectedMediaItem(0, x))
        if item.exceedsFile():
            item.trimToFileBounds()

        item.loop(False)


loopOff()
