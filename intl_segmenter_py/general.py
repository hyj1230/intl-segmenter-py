from .core import findUnicodeRangeIndex
from ._general_data import letter_ranges, alphabetic_ranges, numeric_ranges, mark_ranges


# Check if the given code point is included in Unicode \\p{L} general property
def isLetter(cp: int) -> bool:
    return findUnicodeRangeIndex(cp, letter_ranges) >= 0


# Check if the given code point is included in Unicode \\p{Alphabetic} dervied property
def isAlphabetic(cp: int) -> bool:
    return findUnicodeRangeIndex(cp, alphabetic_ranges) >= 0


# Check if the given code point is included in Unicode \\p{N} general property
def isNumeric(cp: int) -> bool:
    return findUnicodeRangeIndex(cp, numeric_ranges) >= 0


# Check if the given code point is included in Unicode \\p{M} general property
def isMark(cp: int) -> bool:
    return findUnicodeRangeIndex(cp, mark_ranges) >= 0


def isAlphanumeric(cp: int) -> bool:
    return isAlphabetic(cp) or isNumeric(cp)
