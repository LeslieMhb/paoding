from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    openai_api_key: str = "sk-xxx"
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    # Java Service
    java_service_url: str = "http://localhost:8080"

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
