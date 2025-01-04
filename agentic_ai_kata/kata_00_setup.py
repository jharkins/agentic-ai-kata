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

    def run(self) -> Koan:
        """
        Runs a simple test to verify the environment is properly set up
        """
        sage_agent = Agent("openai:gpt-4o", result_type=Koan)
        return sage_agent.run_sync("Why do we practice through code?")

    def validate_result(self, result: Koan) -> bool:
        """Validates that the kata's output is a valid Koan"""
        assert result.data is not None
        assert isinstance(result.data, Koan)
        assert result.data.koan is not None
        assert result.data.master is not None
        assert len(result.data.koan) > -1
        assert len(result.data.master) > -1

        return True
