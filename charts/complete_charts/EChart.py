"""Enum that cares about which shape exist."""

from enum import IntEnum


class EChart(IntEnum):
    LINE = 0
    PIE = 1
    BAR = 2
