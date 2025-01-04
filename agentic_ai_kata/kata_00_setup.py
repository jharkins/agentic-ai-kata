from typing import Dict, Any
from .base import KataBase
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, BaseModel, Field
from pydantic_ai import Agent


class Kata00Settings(BaseSettings):
    OPENAI_API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # This will ignore extra fields in the .env file
    )


class Koan(BaseModel):
    """A koan is a short, pithy statement or question that is used to test a student's understanding of a concept."""

    koan: str = Field(description="A Koan about agentic AI")
    master: str = Field(description="The (obviously fictional) Agentic AI Monk's name")


class SetupKata(KataBase):
    """
    Kata 00: Basic Setup and Environment Verification

    This kata ensures:
    1. Environment variables are properly loaded
    2. API keys are valid
    3. Basic LLM communication works
    """

    def __init__(self):
        self.settings = Kata00Settings()

    def run(self) -> Koan:
        """
        Runs a simple test to verify the environment is properly set up
        """
        sage_agent = Agent("openai:gpt-4o", result_type=Koan)
        return sage_agent.run_sync("Why do we practice through code?")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates the setup was successful"""
        return (
            result.get("success", False)
            and "successful" in result.get("message", "").lower()
        )
