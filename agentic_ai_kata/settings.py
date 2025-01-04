from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class KataSettings(BaseSettings):
    """Base settings class for all katas"""

    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str | None = None

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # This will ignore extra fields in the .env file
    )
