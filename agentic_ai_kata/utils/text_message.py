"""Text Message Conversation Generator and Manager.

This module provides functionality to generate and manage sci-fi themed text message conversations.
It uses LLMs to create entertaining and varied conversations that can be used as test data
or examples in the kata exercises.

Key Features:
    - Generate sci-fi themed SMS conversations using LLMs
    - Save conversations to JSON files for reuse
    - Load existing conversations from storage
    - Manage conversation lifecycle (create, store, load, cleanup)

Example Usage:
    # Generate all example conversations:
    python -m agentic_ai_kata.utils.text_message

    # Use in code:
    conversations = await get_example_conversations()
    for conv in conversations:
        messages = conv.get_messages()
        for msg in messages:
            print(f"{msg.from_} -> {msg.to}: {msg.body}")
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from agentic_ai_kata.settings import settings
from slugify import slugify
import uuid


class MediaObject(BaseModel):
    """Media attachment in a message.

    Used to represent any media files (images, audio, etc.) attached to a message.
    Currently supports URL-based media with MIME type identification.
    """

    url: str = Field(description="URL to the media file")
    type: str = Field(description="Media type (e.g. image/jpeg)")


class TextMessage(BaseModel):
    """A Text Message with metadata and optional attachments.

    Represents a single SMS/text message in a conversation, including:
    - Unique identifier
    - Sender and recipient (in E.164 format)
    - Message content
    - Optional media attachments
    - Optional metadata
    - Creation timestamp

    The 'from' field is handled specially due to Python's keyword restrictions,
    using from_ in code but serializing to 'from' in JSON.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Message ID")
    from_: str = Field(
        alias="from",
        description="Who it's from in E.164 format (e.g. +18015551234)",
        validation_alias="from",
        serialization_alias="from",
    )
    to: str = Field(description="Who it's to in E.164 format (e.g. +18015551234)")
    body: str = Field(description="Message content, less than 1600 characters")
    media: Optional[List[MediaObject]] = Field(description="Media attachments")
    meta: Optional[Dict[str, Any]] = Field(description="Metadata about the message")
    expected_handler: Optional[str] = Field(
        description="The handler that should process this message; used for testing purposes",
        default=None,
    )
    createdAt: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="Creation timestamp in Unix epoch seconds",
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {"examples": [{"from": "+18015551234"}]},
    }


class Conversation(BaseModel):
    """A collection of related text messages forming a conversation.

    Features:
    - Unique conversation identifier
    - Ordered list of messages
    - Methods to add messages and retrieve them in chronological order
    - Topic of the conversation

    The conversation can be serialized to/from JSON for storage and retrieval.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Conversation ID"
    )

    who: Optional[List[dict[str, str]]] = Field(
        description="Who is in the conversation? Key is the name, value is the E.164 phone number.",
    )

    topic: str = Field(
        description="Lowercase slug of the topic of the conversation. Less than 5 words.",
        default="",
    )
    messages: List[TextMessage] = Field(
        default=[], description="Messages in the conversation"
    )

    def add_message(self, from_, to, body, media=None, meta=None):
        """Add a message to the conversation.

        Args:
            from_: Who it's from in E.164 format (e.g. +18015551234)
            to: Who it's to in E.164 format (e.g. +18015551234)
            body: Message content, less than 1600 characters
            media: Optional list of MediaObject attachments
            meta: Optional dictionary of metadata about the message
        """
        self.messages.append(
            TextMessage(from_=from_, to=to, body=body, media=media, meta=meta)
        )

    def get_messages(self):
        """Get all messages in the conversation, sorted by creation time.

        Returns:
            List[TextMessage]: Messages sorted by createdAt timestamp
        """
        return sorted(self.messages, key=lambda x: x.createdAt)


async def fabriate_conversation(theme: str, topic: str) -> Conversation:
    """Generate a sci-fi themed conversation using an LLM.

    Uses an AI agent to create entertaining and varied conversations based on
    a given theme or scenario. The agent is prompted to write in a sci-fi style
    and can expand conversations as needed.

    Args:
        theme: Description or script outline for the conversation
        topic: Topic of the conversation, as a slug

    Returns:
        Conversation: A newly generated conversation matching the theme
    """

    agent_message_crafter = Agent(
        settings.DEFAULT_MODEL,
        result_type=Conversation,
        system_prompt=(
            "You write sci-fi themed text message conversations."
            "Most conversations are 3 to 4 turns, but expand as needed."
            "You will be given a topic or script for the conversation and you will do your best to craft it."
            "If the topic or script is unclear, you use your own script and turn it up to 11."
            "Use the slugify_string tool to slugify the topic of the conversation."
        ),
        retries=3,
    )

    @agent_message_crafter.tool_plain
    def slugify_string(topic: str) -> str:
        """Slugify a string."""
        return slugify(topic)

    return await agent_message_crafter.run(theme)


def get_cache_dir() -> Path:
    """Get the conversations directory for storing generated conversations.

    Creates the directory if it doesn't exist.

    Returns:
        Path: Path to the conversations directory
    """
    conversations_dir = Path(__file__).parent.parent.parent / "conversations"
    conversations_dir.mkdir(parents=True, exist_ok=True)
    return conversations_dir


def load_cached_conversation(filename: str) -> Optional[Conversation]:
    """Load a conversation from the conversations directory if it exists.

    Args:
        filename: Name of the conversation file (without .json extension)

    Returns:
        Optional[Conversation]: The loaded conversation, or None if not found
    """
    cache_file = get_cache_dir() / f"{filename}.json"
    if cache_file.exists():
        with open(cache_file, "r") as f:
            return Conversation.model_validate_json(f.read())
    return None


def save_conversation_to_cache(filename: str, conversation: Conversation):
    """Save a conversation to the conversations directory.

    Args:
        filename: Name to save the conversation as (without .json extension)
        conversation: The conversation to save
    """
    cache_file = get_cache_dir() / f"{filename}.json"
    with open(cache_file, "w") as f:
        f.write(conversation.model_dump_json(indent=2))


async def get_example_conversations() -> List[Conversation]:
    """Get example conversations, either from cache or generate them.

    This is the main interface for other modules to get the example conversations.
    It will:
    1. Try to load each conversation from the conversations directory
    2. If not found, generate it using the LLM
    3. Save newly generated conversations for future use

    Returns:
        List[Conversation]: List of all example conversations
    """
    conversations = []
    examples = {
        "casual_banter": "Two friends, with one telling a friend about a particularly luscious Plumbus.",
        "new_phone_who_dis": "New phone, who dis? but it's between knights of the round table",
        "email_me_a_thing": (
            "A text message between the boss and a new assistant."
            "It's a Monty Python-style sketch, playing out over SMS."
            "The boss wants a report on squanchberries emailed to him ASAP."
            "The assistant checks with the boss, and finds out which email to use."
            "The boss responds with the email address, and reinforces that the report is needed ASAP."
            "The assistant responds with a confirmation that the report will be sent ASAP."
        ),
        "sea_shanty_lookup": (
            "Boss: Could you look up <insert made up scifi sounding disease>?"
            "Assistant: I'll look it up and get back to you."
            "Assistant: I found out more <insert made up scifi sounding disease>."
            "Boss: Ok, go on."
            "Assistant (seashanty): <insert made up scifi sounding disease sea shanty verse>"
        ),
    }

    for name, theme in examples.items():
        conversation = load_cached_conversation(name)
        if conversation is None:
            print(f"Generating conversation: {name}")
            result = await fabriate_conversation(theme, name)
            # Extract the Conversation from the RunResult
            conversation = result.data
            save_conversation_to_cache(name, conversation)
        conversations.append(conversation)

    return conversations


def cleanup_conversations():
    """Remove all existing conversations from the conversations directory."""
    conversations_dir = get_cache_dir()
    if conversations_dir.exists():
        for file in conversations_dir.glob("*.json"):
            print(f"Removing old conversation: {file.name}")
            file.unlink()


async def init_cache():
    """Initialize the conversations by generating all examples.

    This is the main entry point when running this module directly.
    It will:
    1. Check if conversations already exist
    2. If they do, bail out early
    3. If they don't, generate fresh versions of all example conversations
    4. Save them to the conversations directory
    """
    print("Checking for existing conversations...")
    conversations_dir = get_cache_dir()
    if any(conversations_dir.glob("*.json")):
        print("Conversations already exist. Skipping initialization.")
        return

    print("Initializing conversations...")
    await get_example_conversations()
    print("Conversations generated successfully!")


if __name__ == "__main__":
    asyncio.run(init_cache())
