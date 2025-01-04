from typing import Any, Dict

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


class Route(BaseModel):
    """A route classification and its handler"""

    category: str = Field(description="The category this input was classified as")
    confidence: float = Field(description="Confidence score for this classification")
    handler: str = Field(description="The handler that should process this input")


class RoutingResult(BaseModel):
    """Result from the routing system"""

    input: str = Field(description="The original input")
    route: Route = Field(description="The chosen route")
    response: str = Field(description="The response from the chosen handler")


class RoutingKata(KataBase):
    """
    Kata 03: Routing Pattern

    This kata demonstrates:
    1. How to classify inputs into categories
    2. How to route to specialized prompts/tools
    3. How to handle ambiguous or uncertain cases
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the routing pattern"""
        # TODO: Implement routing pattern
        raise NotImplementedError("This kata is not yet implemented")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the routing pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, RoutingResult):
            return False

        # Check we have an input
        if not result.data.input or len(result.data.input) == 0:
            return False

        # Check we have a valid route
        if not isinstance(result.data.route, Route):
            return False

        # Check route fields
        if not result.data.route.category or len(result.data.route.category) == 0:
            return False
        if not 0 <= result.data.route.confidence <= 1:
            return False
        if not result.data.route.handler or len(result.data.route.handler) == 0:
            return False

        # Check we have a response
        if not result.data.response or len(result.data.response) == 0:
            return False

        return True
