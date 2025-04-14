import math
from difflib import SequenceMatcher


def similar(a, b, caseSensitive=False):
    if not caseSensitive:
        a = a.lower()
        b = b.lower()
    return SequenceMatcher(None, a, b).ratio()


def is_rounding_error(a, b):
    return math.isclose(a, b, rel_tol=1e-9)


def greater_than(a, b):
    if not is_rounding_error(a, b):
        if a > b:
            return True
    return False


def less_than(a, b):
    if not is_rounding_error(a, b):
        if a < b:
            return True
    return False
