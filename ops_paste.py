from typing import List

import reaper_python as rp
import tracks
from models import Track


def main() -> None:
    sel_tracks: List[Track] = []
    num_sel_tracks = rp.RPR_CountSelectedTracks2(0, False)
    for i in range(num_sel_tracks):
        found_track = Track(rp.RPR_GetSelectedTrack2(0, i, False))
        sel_tracks.append(found_track)

    tracks.selection.clear()
    if num_sel_tracks > 0:
        sel_tracks[0].set_selected(True)

    # Item: Paste items/tracks
    rp.RPR_Main_OnCommandEx(42398, 0, 0)

    for t in sel_tracks:
        t.set_selected(True)


if __name__ == "__main__":
    main()
