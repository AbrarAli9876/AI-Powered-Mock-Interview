from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.base import Base


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# =========================================================
# FASTAPI DATABASE DEPENDENCY
# =========================================================

def get_db():
    """
    Provide a database session for FastAPI requests.

    The session is automatically closed after
    the request is completed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()