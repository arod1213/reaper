import reaper_python as rp


def console(*args):
    for arg in args:
        rp.RPR_ShowConsoleMsg(f"{arg}\n")
