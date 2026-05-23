import json
import re
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.openrouter import call_openrouter
from services.rag import get_relevant_context

router = APIRouter(prefix="/ai", tags=["ai"])


class ExplainBody(BaseModel):
    code: str
    question: str
    language: str = "python"


class ReviewBody(BaseModel):
    code: str
    language: str = "python"


class HintBody(BaseModel):
    code: str
    problem: str
    language: str = "python"


class ChallengeBody(BaseModel):
    language: str = "python"
    difficulty: str = "beginner"


class ChatBody(BaseModel):
    messages: list[dict[str, Any]]
    language: str = "python"
    context: str = ""


def _extract_tag(text: str, tag: str) -> str:
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


@router.post("/explain")
async def explain(body: ExplainBody):
    try:
        rag_context = "\n".join(get_relevant_context(body.question, body.language))
        messages = [{"role": "user", "content": f"Question: {body.question}\n\nCode:\n{body.code}\n\nContext:\n{rag_context}"}]
        result = await call_openrouter("explain", messages, language=body.language)
        return {"response": result["text"], "model_used": result["model"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review")
async def review(body: ReviewBody):
    try:
        result = await call_openrouter("review", [{"role": "user", "content": body.code}], language=body.language)
        text = result["text"]
        return {
            "praise": _extract_tag(text, "praise"),
            "issues": _extract_tag(text, "issues"),
            "suggestion": _extract_tag(text, "suggestion"),
            "rating": _extract_tag(text, "rating"),
            "model_used": result["model"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hint")
async def hint(body: HintBody):
    try:
        content = f"Problem: {body.problem}\n\nCode:\n{body.code}"
        result = await call_openrouter("hint", [{"role": "user", "content": content}], language=body.language)
        return {"hint": result["text"], "model_used": result["model"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-challenge")
async def generate_challenge(body: ChallengeBody):
    try:
        result = await call_openrouter(
            "challenge", [{"role": "user", "content": "Generate now."}], language=body.language, difficulty=body.difficulty
        )
        return json.loads(result["text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat(body: ChatBody):
    try:
        messages = body.messages
        if body.context:
            messages = [{"role": "system", "content": f"Context: {body.context}"}, *messages]
        result = await call_openrouter("explain", messages, language=body.language)
        return {"response": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
