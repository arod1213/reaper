import reaper_python as rp

class Loop():
  def __init__(self):
    self.is_set, self.isloop, self.start, self.end, self.canseek = rp.RPR_GetSet_LoopTimeRange(False, True, 0, 0, False)
    
  def setLoop(self, start, end):
    rp.RPR_GetSet_LoopTimeRange(True, True, start, end, False)
    
class MediaTrack():
  def __init__(self, track):
    self.id = track
    self.int = int(rp.RPR_GetMediaTrackInfo_Value(self.id, "IP_TRACKNUMBER"))
    self.name = rp.RPR_GetSetMediaTrackInfo_String(self.id, "P_NAME", "", False)[3]
    self.lanestate = rp.RPR_GetMediaTrackInfo_Value(self.id, "C_LANESCOLLAPSED")
    self.lanecount = rp.RPR_GetMediaTrackInfo_Value(self.id, "I_NUMFIXEDLANES")
    
    self.razorBounds = "" # initialize list 0 = start / 1 = end
    
  def razorCheck(self):
    if len(self.razorBounds) != 0:
      x = []
      x = self.razorBounds.split(" ")
      self.razorStart = x[0]
      self.razorEnd = x[1]
  
  def setRazor(self, start, end):
    bounds = "{} {}".format(start,end)
    rp.RPR_GetSetMediaTrackInfo_String(self.id, "P_RAZOREDITS", bounds, True)
    self.razorBounds = bounds

class MediaItem():
  def __init__(self, item):
    self.id = item
    self.start = rp.RPR_GetMediaItemInfo_Value(self.id, "D_POSITION")
    self.length = rp.RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
    self.end = self.start + self.length
    
  def selectItem(self, bool):
    rp.RPR_SetMediaItemSelected(self.id, bool)
    
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
  trackCount = rp.RPR_CountTracks(0)
  selTrackCount = rp.RPR_CountSelectedTracks(0)
  
  lastSelTrack = MediaTrack(rp.RPR_GetSelectedTrack(0, selTrackCount-1))

  if lastSelTrack.int < trackCount:
   rp.RPR_SetOnlyTrackSelected(rp.RPR_GetTrack(0, lastSelTrack.int))
  
def selectedItemExtremeBounds():
  numSelItems = rp.RPR_CountSelectedMediaItems(0)
  index = 1
  item = MediaItem(rp.RPR_GetSelectedMediaItem(0, index-1))
  minStart = item.start # init value
  maxEnd = item.end # init value
  
  while index < numSelItems:
    item = MediaItem(rp.RPR_GetSelectedMediaItem(0, index))
    if item.start < minStart:
      minStart = item.start
    if item.end > maxEnd:
      maxEnd = item.end
    index += 1

  return minStart, maxEnd

def deselectAllItems():
  numSelItems = rp.RPR_CountSelectedMediaItems(0)
  index = numSelItems
  item = MediaItem(rp.RPR_GetSelectedMediaItem(0, index-1))
  while index > 0:
    item.selectItem(False)
    index -= 1
    item = MediaItem(rp.RPR_GetSelectedMediaItem(0, index-1))
  
def moveSelection():
  currentLoop = Loop()
  
  numTracks = rp.RPR_CountTracks(0)
  index = 0
  track = MediaTrack(rp.RPR_GetTrack(0,index)) # get first track

  while len(rp.RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", "", False)[3]) == 0 and index < numTracks:
    index += 1
    track = MediaTrack(rp.RPR_GetTrack(0, index))
    
  track.razorBounds = rp.RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", "", False)[3]

  if len(track.razorBounds) > 0:
    if index < numTracks-1: # as long as not top track
      rp.RPR_Main_OnCommand(42474,0) # set razor edit to loop
      
      trackBelow = MediaTrack(rp.RPR_GetTrack(0, index+1))
      
      if track.lanestate == 0:
        rp.RPR_GetSetMediaTrackInfo_String(trackBelow.id, "P_RAZOREDITS", track.razorBounds, True) # set razor edit up a track
        rp.RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", 0, True) # remove razor edit on previous track
        # EDIT THIS SECTION TO NOT SELECT WHOLE COMP LANES
      else:
        rp.RPR_GetSetMediaTrackInfo_String(trackBelow.id, "P_RAZOREDITS", track.razorBounds, True) # set razor edit up a track
        rp.RPR_GetSetMediaTrackInfo_String(track.id, "P_RAZOREDITS", 0, True) # remove razor edit on previous track
      
      rp.RPR_SetOnlyTrackSelected(trackBelow.id) # move track selection to one above bottom razor edit
      currentLoop.setLoop(currentLoop.start, currentLoop.end) # reset loop position
  else:
    moveTrackSelection()
    MediaTrack(rp.RPR_GetSelectedTrack(0,0)).setRazor(selectedItemExtremeBounds()[0], selectedItemExtremeBounds()[1])
    deselectAllItems()

  

moveSelection() # RUN


  
  
