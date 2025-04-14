from typing import Any

import reaper_python as rp


def console(message: Any):
    rp.RPR_ShowConsoleMsg(f"{message}\n")
