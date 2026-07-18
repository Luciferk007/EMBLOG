from pathlib import Path

from app.modules.can.parser import CANParser

parser = CANParser()

sample_file = Path("app/modules/can/sample_data/candump.log")

frames = parser.parse_file(str(sample_file))

for frame in frames:
    print(frame)