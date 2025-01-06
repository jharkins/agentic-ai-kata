from typing import Any
from dataclasses import dataclass
from openai import AsyncOpenAI

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings


@dataclass
class Deps:
    openai: AsyncOpenAI


class AgentKata(KataBase):
    """
    Kata 07: Full Agent Pattern

    This kata demonstrates:
    1. How to implement autonomous behavior
    2. How to use tools effectively
    3. How to maintain goal-directed behavior
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def run(self) -> Any:
        """Demonstrates the full agent pattern"""
        # TODO: Implement full agent pattern
        raise NotImplementedError("This kata is not yet implemented")
