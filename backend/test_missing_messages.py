from pathlib import Path

from app.modules.can.parser import CANParser
from app.modules.can.analyzer import CANAnalyzer

parser = CANParser()

frames = parser.parse_file(
    str(Path("app/modules/can/sample_data/candump_missing.log"))
)

analyzer = CANAnalyzer(frames)

results = analyzer.detect_missing_messages()

print("=" * 70)
print("Missing Message Detection")
print("=" * 70)

for result in results:
    print(
        f"{result.can_id:<10}"
        f"Expected: {result.expected_period_ms:.2f} ms   "
        f"Largest Gap: {result.largest_gap_ms:.2f} ms   "
        f"Missing: {result.missing_count}"
    )