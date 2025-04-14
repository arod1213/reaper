import math


def db_to_amp(db: float) -> float:
    return 10 ** (db / 20)


def amp_to_db(amp: float) -> float:
    return 20 * math.log10(amp)
