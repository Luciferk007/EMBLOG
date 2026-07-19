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


@dataclass(slots=True)
class CANIDFrequency:
    """
    Frequency statistics for a CAN ID.
    """

    can_id: str
    frame_count: int
    percentage: float


@dataclass(slots=True)
class CANMessageRate:
    """
    Transmission rate statistics for a CAN ID.
    """

    can_id: str
    frame_count: int
    average_period_ms: float
    frequency_hz: float


@dataclass(slots=True)
class CANMissingMessage:
    """
    Represents missing periodic CAN message information.
    """

    can_id: str
    expected_period_ms: float
    largest_gap_ms: float
    missing_count: int


@dataclass(slots=True)
class CANStatistics:
    """
    Statistics generated from parsed CAN frames.
    """

    total_frames: int
    unique_can_ids: int
    interfaces: list[str]
    capture_start_time: float
    capture_end_time: float
    capture_duration: float
    average_dlc: float
    minimum_dlc: int
    maximum_dlc: int

    top_can_ids: list[CANIDFrequency]
    message_rates: list[CANMessageRate]
    missing_messages: list[CANMissingMessage]