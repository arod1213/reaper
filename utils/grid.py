from typing import Literal
from utils.compare import is_rounding_error

import reaper_python as rp

direction = Literal["left", "right"]


def get(location: float, division: float, direction: direction = "right") -> float:
    if division < 0.01:
        raise ValueError("Division too small")
    (
        _,
        _,
        _,
        divisionInOutOptional,
        swingmodeInOutOptional,
        swingamtInOutOptional,
    ) = rp.RPR_GetSetProjectGrid(0, False, 0.0, 0, 0.0)

    # set to division
    rp.RPR_GetSetProjectGrid(
        0, True, division, swingmodeInOutOptional, swingamtInOutOptional
    )

    found_division = location
    deviation = 0.0
    if direction == "right":
        while (
            found_division <= location or is_rounding_error(found_division, location)
        ) and deviation < 10:
            found_division = rp.RPR_SnapToGrid(0, location + deviation)
            deviation += max([min([0.1, 0.1 * division]), 0.001])
    else:
        while (
            found_division >= location or is_rounding_error(found_division, location)
        ) and deviation < 10:
            found_division = rp.RPR_SnapToGrid(0, location - deviation)
            deviation += max([min([0.1, 0.1 * division]), 0.001])

    # reset grid
    rp.RPR_GetSetProjectGrid(
        0, True, divisionInOutOptional, swingmodeInOutOptional, swingamtInOutOptional
    )
    return found_division
