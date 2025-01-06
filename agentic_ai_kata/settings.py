from pydantic import ConfigDict
from pydantic_settings import BaseSettings

import logfire

logfire.configure()


class KataSettings(BaseSettings):
    """Base settings class for all katas"""

    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str | None = None
    DEFAULT_MODEL: str = "openai:gpt-4o"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # This will ignore extra fields in the .env file
    )


# Global settings instance - properly initialized with environment variables
settings = KataSettings()
