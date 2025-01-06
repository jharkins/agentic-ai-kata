from typing import List
from dataclasses import dataclass
from openai import AsyncOpenAI

from pydantic import BaseModel, Field
from pydantic_ai import Tool
import asyncio
from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings
from agentic_ai_kata.utils.text_message import (
    get_example_conversations,
    Conversation,
)
from agentic_ai_kata.utils.routing import classify_text_message


@dataclass
class Deps:
    openai: AsyncOpenAI


class Route(BaseModel):
    """A route classification and its handler.

    The Route class represents the decision made by the routing system. It includes:
    1. The category the input was classified as
    2. The confidence score for that classification
    3. The specific handler that should process this type of input

    High confidence scores (>0.9) indicate clear routing decisions.
    Lower scores might warrant fallback behavior or human review.
    """

    category: str = Field(description="The category this input was classified as")
    confidence: float = Field(description="Confidence score for this classification")
    handler: str = Field(description="The handler that should process this input")


class RoutingResult(BaseModel):
    """Result from the routing system.

    The RoutingResult captures the complete routing workflow:
    1. The original input that was classified
    2. The routing decision that was made
    3. The response from the chosen specialized handler

    This structure allows for:
    - Tracking the complete routing flow
    - Validating routing decisions
    - Analyzing routing performance
    - Debugging routing issues
    """

    input: str = Field(description="The original input")
    route: Route = Field(description="The chosen route")
    response: str = Field(description="The response from the chosen handler")


def tool_func() -> str:
    return "Hello, world!"


mock_tools = [
    Tool(
        tool_func,
        name="search_wikipedia",
        description="Search Wikipedia for a given query",
    ),
    Tool(
        tool_func,
        name="search_rolodex",
        description="Search the rolodex for a given query",
    ),
    Tool(
        tool_func, name="add_to_rolodex", description="Add a new contact to the rolodex"
    ),
    Tool(
        tool_func,
        name="generate_and_email_report",
        description="Generate and email a report",
    ),
    Tool(tool_func, name="conversation", description="Converse with a human"),
    Tool(tool_func, name="summarize_webpage", description="Summarize a webpage"),
]


class AnalysisTestResult(BaseModel):
    conversation: Conversation
    routing_results: List[RoutingResult] = Field(default_factory=list)


class RoutingKata(KataBase):
    """
    Kata 03: Routing Pattern

    The routing pattern classifies inputs and directs them to specialized handlers. This pattern
    enables separation of concerns and optimization of specialized prompts/tools for each type
    of input.

    Key Benefits:
    1. Separation of concerns - each handler can be optimized for its specific task
    2. Better performance - specialized prompts perform better than generic ones
    3. Cost optimization - can route simple tasks to smaller models
    4. Maintainability - easier to add new handlers or modify existing ones

    This kata demonstrates:
    1. How to classify inputs into categories using an LLM
    2. How to route to specialized prompts/tools based on classification
    3. How to handle ambiguous or uncertain cases with confidence scores
    4. How to validate routing decisions

    Example Use Cases:
    - Customer service: Route different query types (refunds, tech support, general questions)
    - Model selection: Route simple tasks to smaller models, complex ones to larger models
    - Tool selection: Choose appropriate tools based on input type (search, email, chat)

    Implementation Notes:
    - Uses a classification agent to determine input type
    - Routes to specialized handlers based on classification
    - Includes confidence scores to handle uncertainty
    - Validates routing decisions against expected handlers
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)

    async def _run_async(self) -> List[AnalysisTestResult]:
        """Demonstrates the routing pattern by handling text messages."""

        # It all starts with a conversation - so let's manufacture some conversations
        conversations = await get_example_conversations()

        results = []

        for c in conversations:
            analysis_test_result = AnalysisTestResult(
                conversation=c,
                routing_results=[],
            )

            message = c.messages[0]

            # Create a copy of the message without expected_handler before classification
            message_for_classification = message.model_copy()
            message_for_classification.expected_handler = None
            classification_result = await classify_text_message(
                message_for_classification, mock_tools
            )

            # Create a proper Route from the classification
            route = Route(
                category=classification_result.data.category,
                confidence=classification_result.data.confidence,
                handler=classification_result.data.handler,
            )

            # Create a RoutingResult (for now with a mock response)
            routing_result = RoutingResult(
                input=message.body,
                route=route,
                response=f"Mock response from {route.handler}",
            )

            print(f"Classification: {classification_result.data}")
            analysis_test_result.routing_results.append(routing_result)
            results.append(analysis_test_result)

        return results

    def validate_result(self, result: List[AnalysisTestResult]) -> bool:
        """Validates that the routing pattern worked correctly"""
        # Check we have a valid result object
        if not result:
            return False

        for r in result:
            assert isinstance(r, AnalysisTestResult)
            assert isinstance(r.conversation, Conversation)

            for routing_result in r.routing_results:
                assert isinstance(routing_result, RoutingResult)
                message = r.conversation.messages[
                    0
                ]  # We're only testing the first message for now

                print(f"Message: {routing_result.input[:50]}...")
                print(f"Handler: {routing_result.route.handler}")
                if message.expected_handler:
                    print(f"Expected Handler: {message.expected_handler}")
                    assert routing_result.route.handler == message.expected_handler, (
                        f"Handler mismatch for message: {routing_result.input[:50]}...\n"
                        f"Expected: {message.expected_handler}\n"
                        f"Got: {routing_result.route.handler}"
                    )
                print()

        return True

    def run(self) -> List[AnalysisTestResult]:
        """Demonstrates the routing pattern"""
        return asyncio.run(self._run_async())
