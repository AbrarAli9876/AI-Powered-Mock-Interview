from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Gemini
    GEMINI_LIVE_API_KEY: str
    GEMINI_EVALUATION_API_KEY: str

    GEMINI_LIVE_MODEL: str
    GEMINI_EVALUATION_MODEL: str

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str | None = None
    FRONTEND_BASE_URL: str = "http://localhost:5173"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()