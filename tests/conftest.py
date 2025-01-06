from typing import Optional

import pytest
from pydantic_settings import BaseSettings
from pathlib import Path
import shutil


class TestSettings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@pytest.fixture(scope="session")
def settings():
    return TestSettings()


def cleanup_cassettes():
    """Remove all VCR cassettes to force re-recording."""
    cassettes_dir = Path(__file__).parent / "cassettes"
    if cassettes_dir.exists():
        print(f"Removing VCR cassettes directory: {cassettes_dir}")
        shutil.rmtree(cassettes_dir)
        print("VCR cassettes removed. Next test run will re-record API calls.")
    else:
        print("No VCR cassettes found.")


if __name__ == "__main__":
    cleanup_cassettes()


@pytest.fixture(scope="session")
def mock_llm_response():
    """Mock LLM responses for testing"""
    return {"choices": [{"message": {"content": "Test response"}}]}


@pytest.fixture
def async_mock_llm_response():
    """Mock async LLM responses for testing"""

    class AsyncResponse:
        async def __call__(self, *args, **kwargs):
            return {"choices": [{"message": {"content": "Async test response"}}]}

    return AsyncResponse()


# Configure VCR
@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with 'DUMMY' in cassettes
        "filter_headers": [("authorization", "DUMMY")],
        # Custom request matcher to handle OpenAI API versioning
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
        # Handle binary/compressed responses
        "decode_compressed_response": True,
        # Don't try to decode binary post data
        "filter_post_data_parameters": None,
        # Record all requests in text mode
        "record_mode": "once",
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    # Store cassettes next to test files
    test_dir = Path(request.module.__file__).parent
    return str(test_dir / "cassettes")
