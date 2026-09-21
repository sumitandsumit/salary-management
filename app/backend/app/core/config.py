"""App configuration. Single source for env-driven settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

PAGE_SIZE_DEFAULT = 25
PAGE_SIZE_MAX = 100


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SALARY_")

    app_name: str = "ACME Salary Management"
    database_url: str = "sqlite:///./salary.db"
    page_size_default: int = PAGE_SIZE_DEFAULT
    page_size_max: int = PAGE_SIZE_MAX
    log_level: str = "INFO"
    request_id_header: str = "X-Request-ID"


settings = Settings()
