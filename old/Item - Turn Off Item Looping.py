def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")
  

class MediaItem():
  
  def __init__(self, item):
    self.id = item
    self.length = RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
    self.take = RPR_GetMediaItemTake(self.id, int(RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE")))
    self.playrate = RPR_GetMediaItemTakeInfo_Value(self.take, "D_PLAYRATE")
    self.filelength = float(self.length * self.playrate)
    self.isloop = RPR_GetMediaItemInfo_Value(self.id, "B_LOOPSRC")
    self.source = RPR_GetMediaItemTake_Source(self.take)
    self.sourcelen = RPR_GetMediaSourceLength(self.source, False)[0]
    self.startoffset = RPR_GetMediaItemTakeInfo_Value(self.take, "D_STARTOFFS")
    
  def loop(self, bool):
    if bool:
      bool = 1
    else:
      bool = 0
    RPR_SetMediaItemInfo_Value(self.id, "B_LOOPSRC", bool)
  
  def exceedsFile(self):
    if self.filelength + self.startoffset > self.sourcelen:
      return True
    else:
      return False
    
  def trimToFileBounds(self):
    #console(self.sourcelen)
    #console(self.startoffset)
    x = (self.sourcelen - self.startoffset) / self.playrate
    RPR_SetMediaItemInfo_Value(self.id, "D_LENGTH", x)


def loopOff():
  #console(RPR_CountSelectedMediaItems(0))
  for x in range(0, RPR_CountSelectedMediaItems(0)):
    item = MediaItem(RPR_GetSelectedMediaItem(0, x))
    if item.exceedsFile():
      item.trimToFileBounds()
      
    item.loop(False)
    
loopOff()
