"""
Data models for DBC database.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DBCSignal:
    """
    Represents a signal inside a CAN message.
    """

    name: str
    start_bit: int
    length: int
    byte_order: str
    value_type: str
    factor: float
    offset: float
    minimum: float
    maximum: float
    unit: str


@dataclass(slots=True)
class DBCMessage:
    """
    Represents a CAN message defined in a DBC.
    """

    can_id: int
    name: str
    dlc: int
    transmitter: str

    signals: list[DBCSignal] = field(default_factory=list)


@dataclass(slots=True)
class DBCDatabase:
    """
    Represents an entire DBC database.
    """

    messages: dict[int, DBCMessage] = field(default_factory=dict)

@dataclass(slots=True)
class DecodedSignal:
    """
    Represents a decoded CAN signal.
    """

    name: str
    value: float
    unit: str

@dataclass(slots=True)
class DecodedMessage:
    """
    Represents a decoded CAN message.
    """

    can_id: int
    message_name: str
    signals: list[DecodedSignal] = field(default_factory=list)