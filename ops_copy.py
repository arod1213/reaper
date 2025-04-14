import items
import razors
import reaper_python as rp
from nav import cursor


def main():
    item_start, item_end = items.find.get_selection_bounds()
    razor_start, razor_end = razors.properties.get_bounds()

    # Decide which bounds to use
    if razor_start is not None and razor_end is not None:
        start_pos, end_pos = razor_start, razor_end
    else:
        start_pos, end_pos = item_start, item_end

    # Set the cursor range if bounds are valid
    if start_pos is not None and end_pos is not None:
        cursor.set(start_pos, isCenter=False)

    # Edit: Copy items/tracks/envelope points (depending on focus) ignoring time selection
    rp.RPR_Main_OnCommandEx(40057, 0, 0)


if __name__ == "__main__":
    main()
