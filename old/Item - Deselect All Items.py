import reaper_python as rp

from models import Item


def deselect():
    numSelItems = rp.RPR_CountSelectedMediaItems(0)
    index = numSelItems

    item = Item(rp.RPR_GetSelectedMediaItem(0, index - 1))
    while index > 0:
        item.set_selected(False)
        index -= 1
        item = Item(rp.RPR_GetSelectedMediaItem(0, index - 1))


deselect()
