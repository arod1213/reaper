def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")

class Loop():
  def __init__(self):
    self.is_set, self.isloop, self.start, self.end, self.canseek = RPR_GetSet_LoopTimeRange(False, True, 0, 0, False)
    
  def setLoop(self, start, end):
    RPR_GetSet_LoopTimeRange(True, True, start, end, False)
    
class MediaTrack():
  def __init__(self, track):
    self.id = track
    self.int = int(RPR_GetMediaTrackInfo_Value(self.id, "IP_TRACKNUMBER"))
    self.name = RPR_GetSetMediaTrackInfo_String(self.id, "P_NAME", "", False)[3]
    self.lanestate = RPR_GetMediaTrackInfo_Value(self.id, "C_LANESCOLLAPSED")
    self.lanecount = RPR_GetMediaTrackInfo_Value(self.id, "I_NUMFIXEDLANES")
    
    self.razorBounds = 0 # initialize list 0 = start / 1 = end
    
  def razorCheck(self):
    if self.razorBounds != 0:
      x = []
      x = self.razorBounds.split(" ")
      self.razorStart = x[0]
      self.razorEnd = x[1]
  
  def setRazor(self, start, end):
    bounds = "{} {}".format(start,end)
    RPR_GetSetMediaTrackInfo_String(self.id, "P_RAZOREDITS", bounds, True)

class MediaItem():
  def __init__(self, item):
    self.id = item
    self.start = RPR_GetMediaItemInfo_Value(self.id, "D_POSITION")
    self.length = RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
    self.end = self.start + self.length
    
  def selectItem(self, bool):
    RPR_SetMediaItemSelected(self.id, bool)
    
  def isInItemInBounds(self, start, end):
    if self.start >+ start and self.end <= end: # inside bounds
      return True
    elif self.start <= start and self.end > start: # bleed left
      return True
    elif self.end >= end and self.start < end: # bleed right
      return True
    else:
      return False


def moveTrackSelection():
  trackCount = RPR_CountSelectedTracks(0)
  
  lastSelTrack = MediaTrack(RPR_GetSelectedTrack(0, trackCount-1))
  
  if lastSelTrack.int > 1:
   RPR_SetOnlyTrackSelected(RPR_GetTrack(0, lastSelTrack.int-2))
  
def selectedItemExtremeBounds():
  numSelItems = RPR_CountSelectedMediaItems(0)
  index = 1
  item = MediaItem(RPR_GetSelectedMediaItem(0, index-1))
  minStart = item.start # init value
  maxEnd = item.end # init value
  
  while index < numSelItems:
    item = MediaItem(RPR_GetSelectedMediaItem(0, index))
    if item.start < minStart:
      minStart = item.start
    if item.end > maxEnd:
      maxEnd = item.end
    index += 1

  return minStart, maxEnd

def deselectAllItems():
  numSelItems = RPR_CountSelectedMediaItems(0)
  index = numSelItems
  item = MediaItem(RPR_GetSelectedMediaItem(0, index-1))
  while index > 0:
    item.selectItem(False)
    index -= 1
    item = MediaItem(RPR_GetSelectedMediaItem(0, index-1))
  
def moveSelection():
  currentLoop = Loop()
  
  numTracks = RPR_CountTracks(0)
  index = numTracks-1
  track = MediaTrack(RPR_GetTrack(0,index)) # get last track

  while len(RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", "", False)[3]) == 0 and index > 0:
    index -= 1
    track = MediaTrack(RPR_GetTrack(0, index))
  
  track.razorBounds = RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", "", False)[3]
  if len(track.razorBounds) > 0:
    if index > 0: # as long as not top track
      RPR_Main_OnCommand(42474,0) # set razor edit to loop
      
      trackAbove = MediaTrack(RPR_GetTrack(0, index-1))
      
      if trackAbove.lanestate == 0:
        RPR_GetSetMediaTrackInfo_String(trackAbove.id, "P_RAZOREDITS", track.razorBounds, True) # set razor edit up a track
        RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", 0, True) # remove razor edit on previous track
        # EDIT THIS SECTION TO NOT SELECT WHOLE COMP LANES
      else:
        RPR_GetSetMediaTrackInfo_String(trackAbove.id, "P_RAZOREDITS", track.razorBounds, True) # set razor edit up a track
        RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", 0, True) # remove razor edit on previous track
      
      RPR_SetOnlyTrackSelected(trackAbove.id) # move track selection to one above bottom razor edit
      currentLoop.setLoop(currentLoop.start, currentLoop.end) # reset loop position
  else:
    moveTrackSelection()
    MediaTrack(RPR_GetSelectedTrack(0,0)).setRazor(selectedItemExtremeBounds()[0], selectedItemExtremeBounds()[1])
    deselectAllItems()

  

moveSelection() # RUN


  
  
