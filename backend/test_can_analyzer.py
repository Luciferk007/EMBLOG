from pathlib import Path

from app.modules.can.analyzer import CANAnalyzer
from app.modules.can.parser import CANParser

parser = CANParser()

frames = parser.parse_file(
    str(Path("app/modules/can/sample_data/candump.log"))
)

stats = CANAnalyzer(frames).analyze()

print("=" * 60)
print("CAN Capture Summary")
print("=" * 60)

print(f"Total Frames      : {stats.total_frames}")
print(f"Unique CAN IDs    : {stats.unique_can_ids}")
print(f"Interfaces        : {stats.interfaces}")
print(f"Capture Duration  : {stats.capture_duration:.3f} sec")
print(f"Average DLC       : {stats.average_dlc}")
print(f"Minimum DLC       : {stats.minimum_dlc}")
print(f"Maximum DLC       : {stats.maximum_dlc}")

print("\nTop CAN IDs")
print("-" * 60)

for item in stats.top_can_ids:
    print(
        f"{item.can_id:>8} | "
        f"Frames: {item.frame_count:<5} | "
        f"{item.percentage:.2f}%"
    )