from pathlib import Path
import tempfile

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.modules.can.service import CANService

router = APIRouter(
    prefix="/can",
    tags=["CAN"]
)

service = CANService()

async def save_uploaded_log(file: UploadFile) -> Path:
    """
    Save uploaded CAN log to a temporary file.
    """

    if not file.filename.endswith(".log"):
        raise HTTPException(
            status_code=400,
            detail="Only .log files are supported.",
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".log",
    ) as temp_file:

        temp_file.write(await file.read())

        return Path(temp_file.name)

async def save_uploaded_dbc(file: UploadFile) -> Path:
    """
    Save uploaded DBC to a temporary file.
    """

    if not file.filename.endswith(".dbc"):
        raise HTTPException(
            status_code=400,
            detail="Only .dbc files are supported.",
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".dbc",
    ) as temp_file:

        temp_file.write(await file.read())

        return Path(temp_file.name)

@router.get("/health")
def health():
    return {"status": "CAN module ready"}


@router.post("/parse")
async def parse_can_log(file: UploadFile = File(...)):
    """
    Upload and parse a candump log.
    """
    temp_path = await save_uploaded_log(file)

    frames = service.parse_log(
        str(temp_path)
    )
    return frames

@router.post("/analyze")
async def analyze_can_log(file: UploadFile = File(...)):
    """
    Upload and analyze a candump log.
    """
    temp_path = await save_uploaded_log(file)

    analysis = service.analyze_log(
        str(temp_path)
    )

    return analysis

@router.post("/decode")
async def decode_can_log(
    log_file: UploadFile = File(...),
    dbc_file: UploadFile = File(...),
):
    """
    Upload a CAN log and DBC file and decode the messages.
    """

    log_path = await save_uploaded_log(
        log_file
    )

    dbc_path = await save_uploaded_dbc(
        dbc_file
    )

    decoded = service.decode_log(
        str(log_path),
        str(dbc_path),
    )
    
    return decoded
