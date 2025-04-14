import reaper_python as rp
from models import Track
import tracks


def main():
    tracks.actions.clear_armed()

    selTracks = rp.RPR_CountSelectedTracks(0)
    armCount = 0
    for i in range(0, selTracks):
        track = Track(rp.RPR_GetSelectedTrack(0, i))
        if track.armed == 1:
            armCount += 1

    if selTracks > 2:
        if armCount * 2 >= selTracks:
            isArm = False
        else:
            isArm = True
    else:
        state = Track(rp.RPR_GetSelectedTrack(0, 0)).armed
        if state == 1:
            isArm = False
        else:
            isArm = True

    for i in range(0, selTracks):
        track = Track(rp.RPR_GetSelectedTrack(0, i))
        track.set_arm(isArm)


if __name__ == "__main__":
    main()  # RUN
