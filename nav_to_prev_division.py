from models import Project
from nav import cursor


def main():
    project = Project(0)
    curr_grid = project.grid
    grid_enabled = project.grid_enabled
    if grid_enabled:
        cursor.move_to_division(curr_grid, "left")
    else:
        cursor.move_by_screen("left")


if __name__ == "__main__":
    main()
