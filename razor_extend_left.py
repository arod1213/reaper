import razors
from models import Project


def main():
    division = Project(0).grid
    razors.set.extend(division=division, target_type="division", direction="left")


if __name__ == "__main__":
    main()
