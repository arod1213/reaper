import reaper_python as rp


def center(onValue: float, minWidth: float = 0.5):
    (proj, isSet, screen_x_start, screen_x_end, start_timeInOut, end_timeInOut) = (
        rp.RPR_GetSet_ArrangeView2(0, False, 0, 0, 0, 0)
    )
    time_length = end_timeInOut - start_timeInOut

    start_pos = onValue - (time_length * 0.5)
    end_pos = onValue + (time_length * 0.5)

    def make_valid(a: float, b: float):
        if a < 0:
            b += a * -1
            a = 0
        return a, b

    start_pos, end_pos = make_valid(start_pos, end_pos)
    while end_pos - start_pos < minWidth:
        end_pos += 0.1
        start_pos -= 0.1
        start_pos, end_pos = make_valid(start_pos, end_pos)

    rp.RPR_GetSet_ArrangeView2(
        0, True, screen_x_start, screen_x_end, start_pos, end_pos
    )
