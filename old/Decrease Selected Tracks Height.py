def console(value):
  RPR_ShowConsoleMsg(value)
  RPR_ShowConsoleMsg("\n")
    
class MediaTrack():
  def __init__(self, track):
    self.id = track
    self.int = int(RPR_GetMediaTrackInfo_Value(self.id, "IP_TRACKNUMBER"))
    self.name = RPR_GetSetMediaTrackInfo_String(self.id, "P_NAME", "", False)[3]
    self.height = RPR_GetMediaTrackInfo_Value(self.id, "I_HEIGHTOVERRIDE")
    
  def changeHeight(self, amount):
    new_height = self.height + amount
    RPR_SetMediaTrackInfo_Value(self.id, "I_HEIGHTOVERRIDE", new_height)
    
def main():
  num_tracks = RPR_CountSelectedTracks(0)
  
  RPR_Undo_BeginBlock2(0) # undo block starts here
  
  for x in range(num_tracks+1):
    track = MediaTrack(RPR_GetSelectedTrack(0, x))
    if track.height > 64:
      track.changeHeight(-40)
  
main()
RPR_TrackList_AdjustWindows(True) # Update the arrangement (often needed)
RPR_PreventUIRefresh(-1)
RPR_UpdateArrange()

RPR_Undo_EndBlock("Decrease All Track Heights", -1)
