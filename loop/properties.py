import reaper_python as rp


def get_selection_bounds() -> tuple[float, float]:
    (proj, isSet, isLoop, startOut, endOut, allowautoseek) = (
        rp.RPR_GetSet_LoopTimeRange2(0, False, False, 0, 0, False)
    )
    return startOut, endOut
