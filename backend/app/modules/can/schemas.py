from pydantic import BaseModel


class CANFrameResponse(BaseModel):
    timestamp: float
    interface: str
    can_id: str
    dlc: int
    data: list[int]