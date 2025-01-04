from typing import Any, Dict
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


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
        self.settings = KataSettings()

    def run(self) -> Any:
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
