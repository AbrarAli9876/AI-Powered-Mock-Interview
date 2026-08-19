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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()