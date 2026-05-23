# CodeMate — AI Pair Programming Learning Platform

CodeMate is a full-stack AI pair programming platform for students learning Python, JavaScript, and C++. It combines a Monaco-powered coding workspace, AI tutoring/review/hints via OpenRouter, challenge progression, and analytics.

## Features
- AI code explanations with structured XML output
- AI code reviews with praise/issues/suggestions/rating
- Socratic hints
- Challenge generation via AI
- Safe Python code execution (5s timeout)
- 60 coding challenges (20 per language)
- Progress dashboard with charts and weak-area tracking
- Optional RAG enrichment via ChromaDB + sentence-transformers

## AI Models Used
- `anthropic/claude-sonnet-4`: Deep explanations + challenge generation
- `deepseek/deepseek-coder`: Code review quality
- `meta-llama/llama-3.1-8b-instruct:free`: Fast lightweight hints
- `google/gemini-flash-1.5`: Bangla-specific route option

## Setup
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## OpenRouter API Key
1. Create an account at https://openrouter.ai/
2. Generate an API key from dashboard settings.
3. Put it in `backend/.env` as `OPENROUTER_API_KEY=...`.

## Screenshot
![CodeMate UI Placeholder](./docs/screenshot-placeholder.png)
