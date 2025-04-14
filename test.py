from models.input import UserInput
from routing.sends import send_sel_tracks_to


def main() -> None:
    user_data = UserInput(title="test", num_inputs=1, caption="send to")
    destination: str | int = user_data.retvals_csv
    if type(destination) is str and destination.isnumeric():
        destination = int(destination)
    send_sel_tracks_to(destination)


if __name__ == "__main__":
    main()


#   returns path of REAPER.exe (not including EXE), i.e. C:\Program Files\REAPER
# Traceback (most recent call last):
#   File "test.py", line 1, in <module>
#     from models.input import UserInput
#   File "/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/models/__init__.py", line 2, in <module>
#     from .item import Item
#   File "/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/models/item.py", line 4, in <module>
#     from .track import Track
#   File "/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/models/track.py", line 2, in <module>
#     from util.gain import amp_to_db, db_to_amp
#   File "/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/util/__init__.py", line 4, in <module>
#     from .track import get_match, get_match_by_name, get_selected
#   File "/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/util/track.py", line 5, in <module>
#     from models import Item, Track
# ImportError: cannot import name 'Item' from partially initialized module 'models' (most likely due to a circular import) (/Users/hollandrodriguez/Library/Application Support/REAPER/Scripts/src/models/__init__.py). Did you mean: 'item'?
