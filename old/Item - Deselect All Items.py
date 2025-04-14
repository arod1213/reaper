def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")


class MediaItem():
  def __init__(self, item):
    self.id = item
    self.start = RPR_GetMediaItemInfo_Value(self.id, "D_POSITION")
    self.length = RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
    self.end = self.start + self.length
    
  def selectItem(self, bool):
    RPR_SetMediaItemSelected(self.id, bool)
    

def deselect():
  numSelItems = RPR_CountSelectedMediaItems(0)
  index = numSelItems

  item = MediaItem(RPR_GetSelectedMediaItem(0, index-1))
  while index > 0:
    item.selectItem(False)
    index -= 1
    item = MediaItem(RPR_GetSelectedMediaItem(0, index-1))

deselect()


  
  
