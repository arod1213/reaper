from models.project import Project
import razors


def main():
    project = Project(0)
    division = project.grid
    razors.set.extend(target_type="division", direction="right", division=division)


if __name__ == "__main__":
    main()
