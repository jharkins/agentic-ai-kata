from typing import Any
from dataclasses import dataclass
from openai import AsyncOpenAI

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings


@dataclass
class Deps:
    openai: AsyncOpenAI


class OrchestratorKata(KataBase):
    """
    Kata 05: Orchestrator-Workers Pattern

    This kata demonstrates:
    1. How to use a central orchestrator to delegate tasks
    2. How to manage dependencies between tasks
    3. How to handle worker failures and retries
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def run(self) -> Any:
        """Demonstrates the orchestrator-workers pattern"""
        # TODO: Implement orchestrator-workers pattern
        raise NotImplementedError("This kata is not yet implemented")
