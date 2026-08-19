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

app.include_router(auth_router)
app.include_router(topic_router)
app.include_router(question_router)
app.include_router(interview_router)
app.include_router(interview_answer_router)
app.include_router(admin_router)
@app.get("/")
def root():
    return {
        "message": "AI Mock Interview API is running successfully."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }