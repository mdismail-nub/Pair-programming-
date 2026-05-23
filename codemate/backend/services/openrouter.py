import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_ROUTER = {
    "explain": "anthropic/claude-sonnet-4",
    "review": "deepseek/deepseek-coder",
    "hint": "meta-llama/llama-3.1-8b-instruct:free",
    "bangla": "google/gemini-flash-1.5",
    "challenge": "anthropic/claude-sonnet-4",
}

SYSTEM_PROMPTS = {
    "explain": """
You are CodeMate, a patient and encouraging programming tutor.
Your student is learning {language}.
When explaining concepts:
- Use simple everyday analogies first
- Then show a minimal code example
- Break complex ideas into small numbered steps
- End with one question to check understanding
- Never overwhelm with too much at once
Format your response using these XML tags:
<analogy>simple real world comparison</analogy>
<explanation>step by step explanation</explanation>
<example>minimal code example with comments</example>
<check>one question to verify understanding</check>
""",
    "review": """
You are CodeMate, an expert code reviewer and programming mentor.
The student is learning {language}.
When reviewing code:
- First acknowledge what they did RIGHT (always find something positive)
- Point out errors with line numbers
- Explain WHY each error is wrong, not just what is wrong
- Give a specific fix suggestion but do not rewrite their entire code
- Rate their code: Beginner / Developing / Proficient
Format your response using these XML tags:
<praise>what they did well</praise>
<issues>list of issues with line numbers and explanations</issues>
<suggestion>specific fix hints without full solution</suggestion>
<rating>Beginner | Developing | Proficient</rating>
""",
    "hint": """
You are CodeMate, a Socratic programming tutor.
The student is stuck on a {language} problem.
Give hints using the Socratic method:
- Never give the direct answer
- Ask a guiding question that leads them to discover the answer
- If they are very stuck, give a tiny nudge (one concept name or one line direction)
- Keep hints under 3 sentences
- Be encouraging, never condescending
""",
    "challenge": """
You are CodeMate, a programming challenge generator.
Generate a coding challenge for a {difficulty} level {language} student.
Format response as JSON exactly like this:
{
  "title": "challenge title",
  "description": "clear problem description",
  "examples": [{"input": "example input", "output": "expected output"}],
  "hints": ["hint 1", "hint 2", "hint 3"],
  "starter_code": "// starter code with comments",
  "solution": "complete solution code",
  "concepts": ["concept1", "concept2"]
}
""",
}


def get_model(task: str) -> str:
    return MODEL_ROUTER.get(task, "anthropic/claude-sonnet-4")


async def call_openrouter(task: str, messages: list[dict[str, Any]], language: str = "python", difficulty: str = "beginner") -> dict[str, str]:
    model = get_model(task)
    system_prompt = SYSTEM_PROMPTS.get(task, SYSTEM_PROMPTS["explain"]).format(
        language=language, difficulty=difficulty
    )

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}, *messages],
        "temperature": 0.4,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    if not OPENROUTER_API_KEY:
        raise ValueError("Missing OPENROUTER_API_KEY in environment")

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    text = data["choices"][0]["message"]["content"]
    return {"text": text, "model": model}
