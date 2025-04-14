from typing import List
import reaper_python as rp


from models import Item


def selItems():
    items = []
    # console(rp.RPR_CountSelectedMediaItems(0))
    for i in reversed(range(0, rp.RPR_CountSelectedMediaItems(0) + 1)):
        items.append(Item(rp.RPR_GetSelectedMediaItem(0, i)))
    return items


def setItemSelect(list: List[Item], isSelect: bool):
    for i in range(0, len(list)):
        list[i].set_selected(isSelect)


def main():
    rp.RPR_Main_OnCommandEx(0, 40513, 0)  # set edit cursor to mouse cursor
    allItems = selItems()
    setItemSelect(allItems, False)


if __name__ == "__main":
    main()
    rp.RPR_UpdateArrange()
