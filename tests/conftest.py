import pytest
from pydantic_settings import BaseSettings
from typing import Optional


class TestSettings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@pytest.fixture(scope="session")
def settings():
    return TestSettings()


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
