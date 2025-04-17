import reaper_python as rp


from utils import console


# ------------------------------------------------------
class MediaItem:
    def __init__(self, item):
        self.id = item
        # self.take = rp.RPR_GetMediaItemTake(self.id, int(RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE")))
        self.parTrack = rp.RPR_GetMediaItemInfo_Value(self.id, "P_TRACK")
        self.start = rp.RPR_GetMediaItemInfo_Value(self.id, "D_POSITION")
        self.length = rp.RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
        self.end = self.start + self.length
        self.fixedlane = rp.RPR_GetMediaItemInfo_Value(self.id, "I_FIXEDLANE")

    def checkTrackSel(self):
        x = rp.RPR_GetMediaTrackInfo_Value(self.parTrack, "I_SELECTED")
        if x == 1:
            return True
        else:
            return False

    def select(self, bool):
        if bool:
            rp.RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 1)
        else:
            rp.RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 0)

    def setRazor(self):
        bounds = "{} {} ''".format(round(self.start, 14), round(self.end, 14))
        rp.RPR_GetSetMediaTrackInfo_String(
            self.parTrack, "P_RAZOREDITS", bounds, True
        )[2]


# -----------------------------------------------------


def selItems():
    items = []
    # console(rp.RPR_CountSelectedMediaItems(0))
    for i in reversed(range(0, rp.RPR_CountSelectedMediaItems(0))):
        items.append(MediaItem(rp.RPR_GetSelectedMediaItem(0, i)))
    return items


def setItemSelect(list, bool):
    for i in range(0, len(list)):
        if isinstance(list[i], MediaItem):
            list[i].select(bool)


# -----------------------------------------------------


def main():
    items = selItems()
    for i in range(0, len(items)):
        editCursor = rp.RPR_GetCursorPosition()
        rp.RPR_MoveEditCursor(
            items[i].start - editCursor, False
        )  # move edit cursor to item

        setItemSelect(items, False)  # deselect all items
        items[i].select(True)
        rp.RPR_Main_OnCommand(40068, 0)  # move item to top lane
        items[i].setRazor()


main()

# console(rp.RPR_GetSetMediaTrackInfo_String(RPR_GetSelectedTrack(0,0), "P_RAZOREDITS", "", False)[3])
rp.RPR_UpdateArrange()
