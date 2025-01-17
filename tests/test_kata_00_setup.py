import pytest
from agentic_ai_kata.kata_00_setup import SetupKata, Koan
from agentic_ai_kata.settings import settings


def test_setup_kata_initialization():
    # Then: It should have a valid API key
    assert settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_setup_kata_run():
    # Given: A configured kata instance
    kata = SetupKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid koan response
    assert kata.validate_result(result)

    # Display the wisdom
    print(f"\nKoan: {result.data.koan}")
    print(f"- {result.data.master}")
