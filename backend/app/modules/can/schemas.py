from pydantic import BaseModel


class CANFrameResponse(BaseModel):
    timestamp: float
    interface: str
    can_id: str
    dlc: int
    data: list[int]

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    total_frames: int
    unique_can_ids: int
    interfaces: list[str]
    capture_start_time: float
    capture_end_time: float
    capture_duration: float
    average_dlc: float
    minimum_dlc: int
    maximum_dlc: int
    top_can_ids: list
    message_rates: list
    missing_messages: list