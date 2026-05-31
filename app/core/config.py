from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AVALAI_API_KEY: str = "aa-nrwSCyPooYb5Qa6dFYLNe8lSfKACa5PnW7cCB4VmMErXL5rD"
    AVALAI_BASE_URL: str = "https://api.avalai.ir/v1"
    AVALAI_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()