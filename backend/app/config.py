from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    clerk_jwks_url: str
    openrouter_api_key: str
    openrouter_model: str = "openai/gpt-4o-mini"
    allowed_origins: str = "http://localhost:3000"
    app_env: str = "local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
