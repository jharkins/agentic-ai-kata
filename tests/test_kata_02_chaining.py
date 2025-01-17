import pytest
from agentic_ai_kata.kata_02_chaining import ChainingKata, ChainResult, ChainStep
from agentic_ai_kata.settings import settings


def test_chaining_kata_initialization():
    # Then: It should have a valid API key
    assert settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_chaining_kata_run():
    # Given: A configured kata instance
    kata = ChainingKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid chain result
    assert kata.validate_result(result)
