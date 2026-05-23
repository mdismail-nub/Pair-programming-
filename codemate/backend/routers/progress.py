from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("")
async def get_progress():
    return {"message": "Use frontend localStorage for demo progress tracking."}
