from app.modules.can.parser import CANParser
from app.modules.can.models import CANFrame
from app.modules.can.analyzer import CANAnalyzer

class CANService:
    """
    Business layer for CAN operations.
    """

    def __init__(self):
        self.parser = CANParser()

    def parse_log(self, file_path: str) -> list[CANFrame]:
        return self.parser.parse_file(file_path)
    
    def analyze_log(self, file_path: str):
        """
        Parse and analyze a CAN log.
        """

        #frames = self.parser.parse_file(file_path)
        frames = self.parse_log(file_path)
        analyzer = CANAnalyzer(frames)

        return analyzer.analyze()