from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "sk-placeholder"
    MODEL_NAME: str = "gpt-4o-mini"
    DATA_DIR: str = "./data"
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"

settings = Settings()
