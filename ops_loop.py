import items
import razors
import reaper_python as rp
from models import Project


def main():
    cursor = Project(0).cursor_pos
    razor_start, razor_end = razors.properties.get_bounds()
    item_start, item_end = items.find.get_selection_bounds()

    start_pos = razor_start or item_start
    end_pos = razor_end or item_end
    if start_pos is None or end_pos is None:
        rp.RPR_GetSet_LoopTimeRange2(0, True, True, cursor, cursor, False)
    else:
        rp.RPR_GetSet_LoopTimeRange2(0, True, True, start_pos, end_pos, False)


if __name__ == "__main__":
    main()
