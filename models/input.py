from dataclasses import dataclass, field

import reaper_python as rp  # or however you're importing rp


@dataclass
class UserInput:
    title: str
    caption: str
    num_inputs: int
    default_value: str = ""
    return_size: int = 512

    retval: bool = field(init=False)
    retvals_csv: str = field(init=False)
    retvals_csv_sz: int = field(init=False)

    def __post_init__(self):
        # This runs automatically *after* __init__ for dataclasses
        self.retval, _, _, _, self.retvals_csv, self.retvals_csv_sz = (
            rp.RPR_GetUserInputs(
                self.title,
                self.num_inputs,
                self.caption,
                self.default_value,
                self.return_size,
            )
        )
        self.retvals_csv = self.retvals_csv.strip()
