import pytest
from agentic_ai_kata.kata_02_chaining import ChainingKata, ChainResult, ChainStep


def test_chaining_kata_initialization():
    # Given: A new kata instance
    kata = ChainingKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_chaining_kata_run():
    # Given: A configured kata instance
    kata = ChainingKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid chain result
    assert kata.validate_result(result)
