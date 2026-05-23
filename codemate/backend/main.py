from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.ai import router as ai_router
from routers.challenges import router as challenges_router
from routers.progress import router as progress_router

app = FastAPI(title="CodeMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
app.include_router(challenges_router)
app.include_router(progress_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
