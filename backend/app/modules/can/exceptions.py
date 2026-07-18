"""
Custom exceptions for CAN parsing.
"""


class CANParserError(Exception):
    """Base exception for CAN parser."""


class InvalidCANFrameError(CANParserError):
    """Raised when a CAN frame is malformed."""