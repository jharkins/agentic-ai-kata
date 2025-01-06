from pydantic import BaseModel, Field
from agentic_ai_kata.utils.text_message import TextMessage
from agentic_ai_kata.settings import settings
from pydantic_ai import Agent, Tool
from typing import List


class TextMessageClassification(BaseModel):
    """A classification of a text message"""

    category: str = Field(description="The category this input was classified as")
    confidence: float = Field(description="Confidence score for this classification")
    handler: str = Field(description="The handler that should process this input")
    reasoning: str = Field(description="The reasoning behind the classification")


async def classify_text_message(
    message: TextMessage, tools: List[Tool]
) -> TextMessageClassification:
    """Classify the text message into a category"""

    tool_string = ",".join([tool.name for tool in tools])

    classification_agent = Agent(
        settings.DEFAULT_MODEL,
        result_type=TextMessageClassification,
        system_prompt=(
            "You are an expert text message classifier and routing assistant. "
            "You are given a text message and you need to classify it into a category. "
            "You should also return the handler that should process this message. "
            "Here is a list of potential tools that can be used as handlers: "
            f"{tool_string}\n\n"
            "Guidelines for classification:\n"
            "1. Use search_rolodex when someone is trying to identify who someone is, asking 'who is this?', or needs contact information\n"
            "2. Use search_wikipedia for general information lookups or research queries\n"
            "3. Use generate_and_email_report for requests to create and send reports\n"
            "4. Use add_to_rolodex when someone is providing their contact information\n"
            "5. Use conversation for general chat that doesn't fit the above categories\n"
            "6. Use summarize_webpage when someone shares a URL or asks about webpage content"
        ),
    )

    classification_result = await classification_agent.run(message.body)

    return classification_result
