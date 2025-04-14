def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")

class Track():
  
  def __init__(self, track):
    self.id = track
    self.isarm = RPR_GetMediaTrackInfo_Value(self.id, "I_RECARM")
    self.name = RPR_GetSetMediaTrackInfo_String(self.id, "P_NAME", "", False)
    self.selected = RPR_GetMediaTrackInfo_Value(self.id, "I_SELECTED")
    
  def arm(self, bool):
    RPR_SetMediaTrackInfo_Value(self.id, "I_RECARM", bool)

def clearUnselectedArms():
  numTracks = RPR_CountTracks(0)
  for x in range(0, numTracks):
    track = Track(RPR_GetTrack(0, x))
    if track.selected == 0:
      track.arm(False)

def toggleArm():
  clearUnselectedArms() # clear old record arms
  
  selTracks = RPR_CountSelectedTracks(0)
  armCount = 0
  for x in range (0, selTracks):
    track = Track(RPR_GetSelectedTrack(0, x))
    if track.isarm == 1:
      armCount += 1
  
  if selTracks > 2:
    if armCount * 2 >= selTracks:
      bool = False
    else:
      bool = True
  else:
    state = Track(RPR_GetSelectedTrack(0, 0)).isarm
    if state == 1:
      bool = False
    else:
      bool = True

  for x in range(0, selTracks):
    track = Track(RPR_GetSelectedTrack(0, x))
    track.arm(bool)


toggleArm() # RUN
