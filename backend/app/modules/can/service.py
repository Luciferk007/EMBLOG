from app.modules.can.parser import CANParser
from app.modules.can.models import CANFrame


class CANService:
    """
    Business layer for CAN operations.
    """

    def __init__(self):
        self.parser = CANParser()

    def parse_log(self, file_path: str) -> list[CANFrame]:
        return self.parser.parse_file(file_path)