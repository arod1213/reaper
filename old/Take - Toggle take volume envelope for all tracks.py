def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")

#------------------------------------------------------
class MediaItem():
  def __init__(self, item):
    self.id = item
    self.take = RPR_GetMediaItemTake(self.id, int(RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE")))
  
  def select(self, bool):
    if bool:
      RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 1)
    else:
      RPR_SetMediaItemInfo_Value(self.id, "B_UISEL", 0)
    
    
    
def saveSelItems():
  selItems = []
  for i in reversed(range(0,RPR_CountSelectedMediaItems(0))):
    selItems.append(MediaItem(RPR_GetSelectedMediaItem(0, i)))
    #selItems[len(selItems)-1].select(False)
  return selItems

def selectAllItems():
  allItems = []
  for i in range(0, RPR_CountMediaItems(0)):
    item = MediaItem(RPR_GetMediaItem(0, i))
    item.select(True)
    allItems.append(item)
    
def deselectAllItems():
  for i in range(0, RPR_CountMediaItems(0)):
    item = MediaItem(RPR_GetMediaItem(0, i))
    item.select(False)

def selectItems(items):
  for i in range(0, len(items)):
    if isinstance(items[i], MediaItem):
      items[i].select(True)
 

def toggleTakeEnvelope():
  selitems = saveSelItems()
  allItems = selectAllItems()
  #RPR_Main_OnCommandEx(0, "_S&M_TAKEENVSHOW9", 0)
  RPR_Main_OnCommand(RPR_NamedCommandLookup("_S&M_TAKEENVSHOW9"),0)
  deselectAllItems()
  selectItems(selitems)

toggleTakeEnvelope()
RPR_UpdateArrange()
