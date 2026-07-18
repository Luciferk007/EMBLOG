from fastapi import APIRouter

router = APIRouter(prefix="/can", tags=["CAN"])


@router.get("/health")
def health():
    return {"status": "CAN module ready"}