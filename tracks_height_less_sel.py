import reaper_python as rp


from models import Track


def main():
    num_tracks = rp.RPR_CountSelectedTracks(0)

    rp.RPR_Undo_BeginBlock2(0)  # undo block starts here

    for x in range(num_tracks + 1):
        track = Track(rp.RPR_GetSelectedTrack(0, x))
        if track.height > 64:
            track.set_height(-40, isAdjust=True)


if __name__ == "__main__":
    main()
    rp.RPR_TrackList_AdjustWindows(True)  # Update the arrangement (often needed)
    rp.RPR_PreventUIRefresh(-1)
    rp.RPR_UpdateArrange()

    rp.RPR_Undo_EndBlock("Decrease All Track Heights", -1)
