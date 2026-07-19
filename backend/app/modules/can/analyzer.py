from collections import Counter

from app.modules.can.models import (
    CANFrame,
    CANStatistics,
    CANIDFrequency,
    CANMessageRate,
    CANMissingMessage,
)


class CANAnalyzer:
    """
    Analyze parsed CAN frames and generate engineering statistics.
    """

    def __init__(self, frames: list[CANFrame]):
        self.frames = frames

    def get_capture_summary(self) -> dict:
        """
        Generate capture level statistics.
        """
        total_frames = len(self.frames)

        interfaces = sorted(
            {frame.interface for frame in self.frames}
        )

        unique_can_ids = len(
            {frame.can_id for frame in self.frames}
        )

        start_time = self.frames[0].timestamp
        end_time = self.frames[-1].timestamp

        duration = end_time - start_time

        dlcs = [frame.dlc for frame in self.frames]

        return {
            "total_frames": total_frames,
            "unique_can_ids": unique_can_ids,
            "interfaces": interfaces,
            "capture_start_time": start_time,
            "capture_end_time": end_time,
            "capture_duration": duration,
            "average_dlc": sum(dlcs) / total_frames,
            "minimum_dlc": min(dlcs),
            "maximum_dlc": max(dlcs),
        }

    def get_can_id_frequency(self) -> list[CANIDFrequency]:
        """
        Calculate CAN ID frequency statistics.
        """
        counter = Counter(frame.can_id for frame in self.frames)

        total_frames = len(self.frames)

        top_ids = []

        for can_id, count in counter.most_common(10):
            percentage = (count / total_frames) * 100

            top_ids.append(
                CANIDFrequency(
                    can_id=can_id,
                    frame_count=count,
                    percentage=percentage,
                )
            )

        return top_ids

    def analyze(self) -> CANStatistics:
        """
        Perform complete CAN log analysis.
        """
        if not self.frames:
            return CANStatistics(
                total_frames=0,
                unique_can_ids=0,
                interfaces=[],
                capture_start_time=0.0,
                capture_end_time=0.0,
                capture_duration=0.0,
                average_dlc=0.0,
                minimum_dlc=0,
                maximum_dlc=0,
                top_can_ids=[],
                message_rates=[],
                missing_messages=[],
            )

        summary = self.get_capture_summary()

        return CANStatistics(
            total_frames=summary["total_frames"],
            unique_can_ids=summary["unique_can_ids"],
            interfaces=summary["interfaces"],
            capture_start_time=summary["capture_start_time"],
            capture_end_time=summary["capture_end_time"],
            capture_duration=summary["capture_duration"],
            average_dlc=summary["average_dlc"],
            minimum_dlc=summary["minimum_dlc"],
            maximum_dlc=summary["maximum_dlc"],
            top_can_ids=self.get_can_id_frequency(),
            message_rates=self.get_message_rate(),
            missing_messages=self.detect_missing_messages(),
        )
    
    def group_frames_by_can_id(self) -> dict[str, list[CANFrame]]:
        """
        Group all CAN frames by CAN ID.
        """
        grouped_frames = {}

        for frame in self.frames:
            grouped_frames.setdefault(frame.can_id, []).append(frame)

        return grouped_frames

    def get_message_rate(self) -> list[CANMessageRate]:
        """
        Calculate the average transmission period and frequency
        for each CAN ID.
        """

        grouped_frames = self.group_frames_by_can_id()

        message_rates = []

        for can_id, frames in grouped_frames.items():

            # Only one frame -> cannot calculate interval
            if len(frames) < 2:
                message_rates.append(
                    CANMessageRate(
                        can_id=can_id,
                        frame_count=len(frames),
                        average_period_ms=0.0,
                        frequency_hz=0.0,
                    )
                )
                continue

            intervals = []

            for index in range(1, len(frames)):
                interval = (
                    frames[index].timestamp
                    - frames[index - 1].timestamp
                )
                intervals.append(interval)

            average_interval = sum(intervals) / len(intervals)

            average_period_ms = average_interval * 1000

            frequency_hz = (
                1 / average_interval
                if average_interval > 0
                else 0.0
            )

            message_rates.append(
                CANMessageRate(
                    can_id=can_id,
                    frame_count=len(frames),
                    average_period_ms=average_period_ms,
                    frequency_hz=frequency_hz,
                )
            )

        return message_rates
    def detect_missing_messages(self) -> list[CANMissingMessage]:
        """
        Detect missing periodic CAN messages by analyzing timestamp gaps.
        """

        grouped_frames = self.group_frames_by_can_id()

        missing_messages = []

        for can_id, frames in grouped_frames.items():

            # Need at least 3 frames to detect a missing message
            if len(frames) < 3:
                continue

            intervals = []

            for index in range(1, len(frames)):
                interval = (
                    frames[index].timestamp
                    - frames[index - 1].timestamp
                )
                intervals.append(interval)

            # Convert to milliseconds
            intervals_ms = [interval * 1000 for interval in intervals]

            # Expected period = smallest interval
            expected_period_ms = min(intervals_ms)

            largest_gap_ms = max(intervals_ms)

            missing_count = 0

            if largest_gap_ms > expected_period_ms:
                missing_count = (
                    round(largest_gap_ms / expected_period_ms) - 1
                )

            if missing_count > 0:
                missing_messages.append(
                    CANMissingMessage(
                        can_id=can_id,
                        expected_period_ms=expected_period_ms,
                        largest_gap_ms=largest_gap_ms,
                        missing_count=missing_count,
                    )
                )

        return missing_messages
    