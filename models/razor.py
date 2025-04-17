from typing import Optional

import reaper_python as rp


class Razor:
    start: Optional[float]
    end: Optional[float]

    def __init__(self, track):
        self.track = track
        data = rp.RPR_GetSetMediaTrackInfo_String(track, "P_RAZOREDITS", "", False)[
            3
        ].split()
        if len(data) > 0:
            self.start = float(data[0])
            self.end = float(data[1])
        else:
            self.start = None
            self.end = None
        # console(self.start)
        # console(self.end)
        self.exists = self.start is not None and self.end is not None
