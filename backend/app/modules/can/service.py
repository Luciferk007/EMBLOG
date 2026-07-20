from app.modules.can.parser import CANParser
from app.modules.can.analyzer import CANAnalyzer
from app.modules.can.dbc_parser import DBCParser
from app.modules.can.decoder import CANDecoder

from app.modules.can.models import (
    CANFrame,
    CANStatistics,
)

from app.modules.can.dbc_models import (
    DecodedMessage,
)

class CANService:
    """
    Business layer for CAN operations.
    """

    def __init__(self):
        self.parser = CANParser()
        self.dbc_parser = DBCParser()
    def parse_log(self, file_path: str) -> list[CANFrame]:
        return self.parser.parse_file(file_path)
    
    def analyze_log(self,file_path: str,) -> CANStatistics:
        """
        Parse and analyze a CAN log.
        """
        frames = self.parse_log(file_path)
        analyzer = CANAnalyzer(frames)

        return analyzer.analyze()
    def decode_log(self,log_file: str,dbc_file: str,) -> list[DecodedMessage]:
        """
        Decode an entire CAN log using a DBC file.
        """

        frames = self.parser.parse_file(log_file)

        database = self.dbc_parser.parse_file(dbc_file)

        decoder = CANDecoder(database)

        decoded_messages = []

        for frame in frames:

            decoded = decoder.decode_frame(frame)

            if decoded is not None:
                decoded_messages.append(decoded)

        return decoded_messages