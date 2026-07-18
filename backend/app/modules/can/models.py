"""
Data models for CAN frames.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CANFrame:
    """
    Represents a single CAN frame.
    """

    timestamp: float
    interface: str
    can_id: str
    dlc: int
    data: list[int]