from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",          # ignore any env vars you haven't declared
        case_sensitive=False,    # allow OPENAI_MODEL or openai_model
    )

    APP_NAME: str = "Signal Room"
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    AI_MODE: str = "mock" # mock | openai
    EMBEDDINGS_MODE: str = "local" # local | openai
    PORT: int = 8000


settings = Settings()
