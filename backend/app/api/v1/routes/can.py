from pathlib import Path
import tempfile

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.modules.can.service import CANService

router = APIRouter(
    prefix="/can",
    tags=["CAN"]
)

service = CANService()


@router.get("/health")
def health():
    return {"status": "CAN module ready"}


@router.post("/parse")
async def parse_can_log(file: UploadFile = File(...)):
    """
    Upload and parse a candump log.
    """

    if not file.filename.endswith(".log"):
        raise HTTPException(
            status_code=400,
            detail="Only .log files are supported."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
        temp_file.write(await file.read())
        temp_path = Path(temp_file.name)

    frames = service.parse_log(str(temp_path))

    return frames
@router.post("/analyze")
async def analyze_can_log(file: UploadFile = File(...)):
    """
    Upload and analyze a candump log.
    """

    if not file.filename.endswith(".log"):
        raise HTTPException(
            status_code=400,
            detail="Only .log files are supported."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
        temp_file.write(await file.read())
        temp_path = Path(temp_file.name)

    analysis = service.analyze_log(str(temp_path))

    return analysis