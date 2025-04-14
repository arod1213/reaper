import reaper_python as rp
import tracks
from models import Track


def send_to_track(send_from: Track, send_to: Track) -> bool:
    if send_from.track == send_to.track:
        return False
    return bool(rp.RPR_CreateTrackSend(send_from.track, send_to.track))


def send_track_to(send_from: Track, destination: str | int) -> bool:
    """Sends all selected tracks to the track that matches the destination

    Args:
        destination (str): Can be a track name or a track number

    Returns:
        bool: True if sends were created
    """
    match_track = tracks.find.get_match(destination)

    if not match_track:
        return False
    return send_to_track(send_from, match_track)


def send_sel_tracks_to(destination: str | int) -> bool:
    """Sends all selected tracks to the track that matches the destination

    Args:
        destination (str): Can be a track name or a track number

    Returns:
        bool: True if sends were created
    """
    match_track = tracks.find.get_match(destination)

    if not match_track:
        return False

    num_sel_tracks = rp.RPR_CountSelectedTracks(0)
    if num_sel_tracks == 0:
        return False
    for i in range(num_sel_tracks):
        sel_track = Track(rp.RPR_GetSelectedTrack(0, i))
        send_to_track(sel_track, match_track)
    return True
