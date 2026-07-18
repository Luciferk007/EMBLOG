"""
CAN log parser.
"""

from pathlib import Path

from .models import CANFrame

from .exceptions import InvalidCANFrameError

class CANParser:
    """
    Parser for Linux candump log files.
    """

    def parse_file(self, file_path: str) -> list[CANFrame]:
        """
        Parse an entire candump log file.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        frames: list[CANFrame] = []

        with path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                frame = self.parse_line(line)
                frames.append(frame)

        return frames

    def parse_line(self, line: str) -> CANFrame:
        """
        Parse a single candump log line.
        """

        try:
            timestamp_part, rest = line.split(") ", 1)
            timestamp = float(timestamp_part.strip("("))

            interface, frame = rest.split(" ", 1)
            can_id, data_hex = frame.split("#")

            data = [
                int(data_hex[i:i + 2], 16)
                for i in range(0, len(data_hex), 2)
            ]

            dlc = len(data)

            return CANFrame(
                timestamp=timestamp,
                interface=interface,
                can_id=can_id,
                dlc=dlc,
                data=data,
            )

        except Exception as exc:
            raise InvalidCANFrameError(
                f"Invalid CAN frame: {line}"
            ) from exc