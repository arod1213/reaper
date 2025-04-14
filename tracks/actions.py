import reaper_python as rp
from models import Track

def clear_armed():
  numTracks = rp.RPR_CountTracks(0)
  for i in range(0, numTracks):
    track = Track(rp.RPR_GetTrack(0, i))
    track.set_arm(False)
