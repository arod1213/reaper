import items
import razors
import reaper_python as rp
import tracks
from models import Project


def main():
    project = Project(0)
    item_start, item_end = items.find.get_selection_bounds()
    razor_start, razor_end, _ = razors.properties.get_bounds()

    # Use razor bounds if available, otherwise use item bounds
    start_pos, end_pos = (
        (razor_start, razor_end)
        if razor_start is not None and razor_end is not None
        else (item_start, item_end)
    )

    # If no bounds are available, set context to tracks
    prev_track = None
    if start_pos is None or end_pos is None:
        project.set_context("tracks")
        first_sel_track = tracks.find.get_selected(position="first")
        if not first_sel_track:
            return None
        if first_sel_track.number > 1:
            prev_track = tracks.find.get(first_sel_track.number - 1)

    # Cut items/tracks/envelope points (depending on focus) ignoring time selection
    rp.RPR_Main_OnCommandEx(40059, 0, 0)

    # Restore razor bounds if they exist
    if start_pos is not None and end_pos is not None:
        razors.set.set_to_bounds(start_pos, end_pos)

    # select prev track
    if prev_track is not None:
        prev_track.set_selected(True)


if __name__ == "__main__":
    rp.RPR_Undo_BeginBlock()
    main()
    rp.RPR_Undo_EndBlock("Cut", 0)
