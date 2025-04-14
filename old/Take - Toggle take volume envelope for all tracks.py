import reaper_python as rp


class MediaItem:
    def __init__(self, item):
        self.id = item
        self.take = rp.RPR_GetMediaItemTake(
            self.id, int(rp.RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE"))
        )

    def select(self, bool):
        if bool:
            rp.RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 1)
        else:
            rp.RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 0)


def saveSelItems():
    selItems = []
    for i in reversed(range(0, rp.RPR_CountSelectedMediaItems(0))):
        selItems.append(MediaItem(rp.RPR_GetSelectedMediaItem(0, i)))
        # selItems[len(selItems)-1].select(False)
    return selItems


def selectAllItems():
    allItems = []
    for i in range(0, rp.RPR_CountMediaItems(0)):
        item = MediaItem(rp.RPR_GetMediaItem(0, i))
        item.select(True)
        allItems.append(item)


def deselectAllItems():
    for i in range(0, rp.RPR_CountMediaItems(0)):
        item = MediaItem(rp.RPR_GetMediaItem(0, i))
        item.select(False)


def selectItems(items):
    for i in range(0, len(items)):
        if isinstance(items[i], MediaItem):
            items[i].select(True)


def toggleTakeEnvelope():
    selitems = saveSelItems()
    allItems = selectAllItems()
    # rp.RPR_Main_OnCommandEx(0, "_S&M_TAKEENVSHOW9", 0)
    rp.RPR_Main_OnCommand(rp.RPR_NamedCommandLookup("_S&M_TAKEENVSHOW9"), 0)
    deselectAllItems()
    selectItems(selitems)


toggleTakeEnvelope()
rp.RPR_UpdateArrange()
