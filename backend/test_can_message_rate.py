from pathlib import Path

from app.modules.can.parser import CANParser
from app.modules.can.analyzer import CANAnalyzer

parser = CANParser()

frames = parser.parse_file(
    str(Path("app/modules/can/sample_data/candump_periodic.log"))
)

analyzer = CANAnalyzer(frames)

rates = analyzer.get_message_rate()

print("=" * 65)
print("CAN Message Rate")
print("=" * 65)

print(
    f"{'CAN ID':<10}"
    f"{'Frames':<10}"
    f"{'Period(ms)':<18}"
    f"{'Frequency(Hz)':<18}"
)

print("-" * 65)

for rate in rates:
    print(
        f"{rate.can_id:<10}"
        f"{rate.frame_count:<10}"
        f"{rate.average_period_ms:<18.2f}"
        f"{rate.frequency_hz:<18.2f}"
    )