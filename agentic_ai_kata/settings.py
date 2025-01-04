from pydantic import ConfigDict
from pydantic_settings import BaseSettings

import logfire

logfire.configure()


class KataSettings(BaseSettings):
    """Base settings class for all katas"""

    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str | None = None

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # This will ignore extra fields in the .env file
    )

    @classmethod
    def get_settings(cls) -> "KataSettings":
        """
        Get settings instance with environment variables loaded.

        Returns:
            KataSettings: Configured settings instance
        """
        return cls.model_validate({})
