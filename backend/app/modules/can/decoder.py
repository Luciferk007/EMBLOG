"""
CAN signal decoder using DBC definitions.
"""

from app.modules.can.models import CANFrame
from app.modules.can.dbc_models import (
    DBCDatabase,
    DBCSignal,
    DecodedMessage,
    DecodedSignal,
)


class CANDecoder:
    """
    Decode CAN frames using a parsed DBC database.
    """

    def __init__(self, database: DBCDatabase):
        self.database = database

    def _extract_raw_value(self,frame: CANFrame,signal: DBCSignal,) -> int:
        """
        Extract raw integer value from CAN frame.
        """
        if signal.byte_order == "1":
            return self._extract_intel_raw(frame,signal,)

        raise NotImplementedError(
        "Motorola byte order is not yet supported."
    )
    def _extract_intel_raw(self,frame: CANFrame,signal: DBCSignal,) -> int:
        """
        Extract Intel (Little Endian) signal.
        """
        data = bytes(frame.data)

        raw_data = int.from_bytes(
            data,
            byteorder="little",
        )

        mask = (1 << signal.length) - 1

        raw_value = (
            raw_data >> signal.start_bit
        ) & mask

        return raw_value    

    def _apply_scaling(self,raw_value: int,signal: DBCSignal,) -> float:
        """
        Apply DBC scaling (factor and offset).
        """

        return (
            raw_value * signal.factor
        ) + signal.offset

    def _calculate_physical_value(self,raw_value: int,signal: DBCSignal,) -> float:
        """
        Convert raw CAN value into physical engineering value.
        """

        return self._apply_scaling(
            raw_value,
            signal,
        )

    def _decode_signal(
        self,
        frame: CANFrame,
        signal: DBCSignal,
    ) -> DecodedSignal:
        """
        Decode a single CAN signal.
        """

        raw_value = self._extract_raw_value(
            frame,
            signal,
        )

        engineering_value = self._calculate_physical_value(raw_value,signal,)

        return DecodedSignal(
            name=signal.name,
            value=engineering_value,
            unit=signal.unit,
        )

    def decode_frame(
        self,
        frame: CANFrame,
    ) -> DecodedMessage | None:
        """
        Decode a single CAN frame.
        """

        can_id = int(frame.can_id, 16)

        message = self.database.messages.get(can_id)

        if message is None:
            return None

        decoded_signals = []

        for signal in message.signals:

            decoded_signal = self._decode_signal(
                frame,
                signal,
            )

            decoded_signals.append(decoded_signal)

        return DecodedMessage(
            can_id=message.can_id,
            message_name=message.name,
            signals=decoded_signals,
        )