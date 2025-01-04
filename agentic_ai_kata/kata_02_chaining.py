from typing import Any

from pydantic import BaseModel, Field

from agentic_ai_katabase import KataBase
from agentic_ai_katasettings import KataSettings


class ChainStep(BaseModel):
    """A single step in a chain of prompts"""

    prompt: str = Field(description="The prompt for this step")
    response: str = Field(description="The response from the LLM")
    next_step: str | None = Field(description="The next step to take, if any")


class ChainResult(BaseModel):
    """Result from a chain of prompts"""

    steps: list[ChainStep] = Field(description="The steps in the chain")
    final_result: str = Field(description="The final result after all steps")


class ChainingKata(KataBase):
    """
    Kata 02: Prompt Chaining Pattern

    This kata demonstrates:
    1. How to decompose tasks into multiple LLM calls
    2. How to chain prompts together with optional gating/checks
    3. How to handle errors and retries in chains
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the prompt chaining pattern"""
        # TODO: Implement prompt chaining pattern
        raise NotImplementedError("This kata is not yet implemented")
