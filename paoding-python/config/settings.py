from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM (Alibaba Cloud DashScope - DeepSeek)
    openai_api_key: str = "sk-7943a03e14bf4b379116412e66fd4142"
    openai_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    openai_model: str = "deepseek-v4-pro"

    # Java Service
    java_service_url: str = "http://localhost:8080"

    # Langfuse Observability
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = False

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
