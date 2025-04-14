import items
import razors


def main():
    start_pos, end_pos = razors.properties.get_bounds()
    if start_pos is None or end_pos is None:
        return
    items.find.clear()
    items.selection.select_items_in_bounds(start_pos, end_pos)


if __name__ == "__main__":
    main()
