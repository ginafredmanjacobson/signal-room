from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings (BaseSettings):
    APP_NAME: str = "SignalRoom"
    DEBUG: bool = False


    DATABASE_URL: str = "sqlite:///./signalroom.db"

    OPENAI_AI_KEY: str = ""
    AI_MODE: str = "mock" # "live" or "mock"

    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "SIgalRoom/1.0"

    RSS_FEEDS: str = ""

    model_config + ConfigDict(env_file=".env", extra="ignore")


settings = Settings()

