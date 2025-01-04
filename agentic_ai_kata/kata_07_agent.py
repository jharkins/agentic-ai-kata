from typing import Any, Dict

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


class AgentThought(BaseModel):
    """A single thought in the agent's reasoning process"""

    thought: str = Field(description="The agent's internal thought")
    action: str = Field(description="The action the agent decided to take")
    observation: str = Field(
        description="What the agent observed after taking the action"
    )


class AgentResult(BaseModel):
    """Result from the agent's execution"""

    thoughts: list[AgentThought] = Field(description="The agent's thought process")
    final_answer: str = Field(description="The agent's final answer")
    tools_used: list[str] = Field(description="Tools the agent used")


class AgentKata(KataBase):
    """
    Kata 07: Full Agent Pattern

    This kata demonstrates:
    1. How to create an autonomous agent that can plan and act
    2. How to use tools effectively
    3. How to maintain goal-directed behavior
    4. How to handle errors and unexpected situations
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the full agent pattern"""
        # TODO: Implement full agent pattern
        raise NotImplementedError("This kata is not yet implemented")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the agent pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, AgentResult):
            return False

        # Check we have thoughts
        if not result.data.thoughts or len(result.data.thoughts) == 0:
            return False

        # Check each thought
        for thought in result.data.thoughts:
            if not isinstance(thought, AgentThought):
                return False
            if not thought.thought or len(thought.thought) == 0:
                return False
            if not thought.action or len(thought.action) == 0:
                return False
            if not thought.observation or len(thought.observation) == 0:
                return False

        # Check final answer
        if not result.data.final_answer or len(result.data.final_answer) == 0:
            return False

        # Check tools were used
        if not result.data.tools_used or len(result.data.tools_used) == 0:
            return False

        return True
