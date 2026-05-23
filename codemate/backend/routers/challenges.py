import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.code_runner import run_python_code

router = APIRouter(prefix="/challenges", tags=["challenges"])

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "challenges.json"


class RunBody(BaseModel):
    code: str
    language: str = "python"


@router.get("")
async def list_challenges():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.post("/run")
async def run_challenge(body: RunBody):
    if body.language.lower() != "python":
        raise HTTPException(status_code=400, detail="Demo runner currently supports Python only")
    return run_python_code(body.code)
