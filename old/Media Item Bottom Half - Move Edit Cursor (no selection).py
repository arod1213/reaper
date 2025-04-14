def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")

#-----------------------------------

class MediaItem():
  def __init__(self, item):
    self.id = item
    self.take = RPR_GetMediaItemTake(self.id, int(RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE")))
  
  def select(self, bool):
    if bool:
      RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 1)
    else:
      RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 0)


#-----------------------------------

def selItems():
  items = []
  #console(RPR_CountSelectedMediaItems(0))
  for i in reversed(range(0,RPR_CountSelectedMediaItems(0)+1)):
    items.append(MediaItem(RPR_GetSelectedMediaItem(0, i)))
  return items

def setItemSelect(list, bool):
  for i in range(0,len(list)):
    if isinstance(list[i], MediaItem):
      list[i].select(bool)

def main():
  #items = []
  #items = selItems()
  RPR_Main_OnCommandEx(0, 40513, 0) # set edit cursor to mouse cursor
  allItems = selItems()
  setItemSelect(allItems, False)
  #setItemSelect(items, True)

#console('test')
main()
RPR_UpdateArrange()
