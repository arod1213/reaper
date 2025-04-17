import reaper_python as rp

import items
import razors
from nav import cursor


def select(start_pos, end_pos):
    start_pos = float(start_pos or 0)
    end_pos = float(end_pos or 0)
    items.selection.select_items_in_bounds(start_pos, end_pos)


def main():
    item_start, item_end = items.find.get_selection_bounds()
    razor_start, razor_end, razor_exists = razors.properties.get_bounds()
    # Decide which bounds to use
    if razor_exists:
        start_pos, end_pos = razor_start, razor_end
        rp.RPR_SetCursorContext(1, "")
    else:
        start_pos, end_pos = item_start, item_end
    # Set the cursor range if bounds are valid
    if start_pos is not None and end_pos is not None:
        cursor.set(start_pos, isCenter=False)

    # Edit: Copy items/tracks/envelope points (depending on focus) ignoring time selection
    rp.RPR_Main_OnCommandEx(40057, 0, 0)

    if razor_exists:
        select(razor_start, razor_end)


if __name__ == "__main__":
    main()
