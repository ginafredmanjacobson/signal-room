from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Signal Room"
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
