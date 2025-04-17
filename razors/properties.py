import reaper_python as rp
from models import Track


def get_bounds() -> tuple[float | None, float | None, bool]:
    num_tracks = rp.RPR_CountTracks(0)
    start_pos, end_pos = None, None
    for i in range(num_tracks):
        track = Track(rp.RPR_GetTrack(0, i))
        if track.razor.start is None or track.razor.end is None:
            continue
        if start_pos is None or track.razor.start < start_pos:
            start_pos = track.razor.start
        if end_pos is None or track.razor.end > end_pos:
            end_pos = track.razor.end

    exists = start_pos is not None and end_pos is not None
    if exists:
        start_pos = float(start_pos or 0)
        end_pos = float(end_pos or 0)
    return start_pos, end_pos, exists
