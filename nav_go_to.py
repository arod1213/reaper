import reaper_python as rp
from nav import go_to


def main():
    (retval, title, num_inputs, captions_csv, retvals_csv, retvals_csv_sz) = (
        rp.RPR_GetUserInputs(
            "Go To", 1, "prefix (m for measure) (` for track):", "", 25
        )
    )
    location = retvals_csv.strip()
    if location == "":
        return
    location_type = location[0]
    destination = location[1:]
    match location_type:
        case "m":
            location_type = "measure"
        case "`":
            location_type = "track"

    if destination.replace(".", "").isnumeric():
        destination = int(round(float(destination)))
    go_to(location_type, value=destination)


if __name__ == "__main__":
    main()
