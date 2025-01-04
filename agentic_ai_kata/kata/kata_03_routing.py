from typing import Any

from pydantic import BaseModel, Field

from ..base import KataBase
from ..settings import KataSettings


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
