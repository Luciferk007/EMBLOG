from pathlib import Path

from app.modules.can.parser import CANParser

parser = CANParser()

sample_file = Path("app/modules/can/sample_data/candump.log")

frames = parser.parse_file(str(sample_file))

for frame in frames:
    print(frame.can_id,frame.is_extended)
print("\nExtended Frames")

frames = CANParser().parse_file(
    "app/modules/can/sample_data/candump_extended.log"
)

for frame in frames:
    print(frame.can_id,frame.is_extended)