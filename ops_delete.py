import items
import razors
import reaper_python as rp
import tracks
from models import Project


def main():
    item_start, item_end = items.find.get_selection_bounds()
    razor_start, razor_end = razors.properties.get_bounds()
    project = Project(0)
    context = project.cursor_context
    if (
        context != "tracks"
        and rp.RPR_CountSelectedMediaItems(project.project) == 0
        and razor_start is None
    ):
        project.set_context("tracks")
    elif context == "tracks" and (razor_start is not None or item_start is not None):
        project.set_context("items")

    prev_track = None
    if context == "tracks":
        first_sel_track = tracks.find.get_selected(position="first")
        if first_sel_track.number > 1:
            prev_track = tracks.find.get(first_sel_track.number - 1)

    # Remove items/tracks/envelope points (depending on focus)
    rp.RPR_Main_OnCommandEx(40697, 0, 0)

    # select prev track
    if prev_track is not None:
        prev_track.set_selected(True)


if __name__ == "__main__":
    rp.RPR_Undo_BeginBlock()
    main()
    rp.RPR_Undo_EndBlock("Delete", 0)
