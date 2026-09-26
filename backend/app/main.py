from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_routes import router as auth_router
from app.api.topic_routes import router as topic_router
from app.api.question_routes import router as question_router
from app.api.interview_routes import router as interview_router
from app.api.interview_answer_routes import (
    router as interview_answer_router,
)
from app.api.admin_routes import router as admin_router
from app.api.coding_question_routes import (
    router as coding_question_router,
)
from app.api.code_execution_routes import (
    router as code_execution_router,
)
from app.api.coding_interview_routes import (
    router as coding_interview_router,
)


app = FastAPI(
    title="AI Mock Interview API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)

app.include_router(topic_router)

app.include_router(question_router)

app.include_router(interview_router)

app.include_router(interview_answer_router)

app.include_router(admin_router)

app.include_router(coding_question_router)

app.include_router(code_execution_router)

app.include_router(coding_interview_router)
# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "AI Mock Interview API is running successfully."
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }