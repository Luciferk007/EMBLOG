"""
CAN log parser.
"""

from pathlib import Path

from .models import CANFrame


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
        Parse a single CAN frame.

        To be implemented next.
        """
        raise NotImplementedError