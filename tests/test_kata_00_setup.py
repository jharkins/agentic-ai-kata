import pytest
from agentic_ai_kata.kata.kata_00_setup import SetupKata, Koan


def test_setup_kata_initialization():
    # Given: A new kata instance
    kata = SetupKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


def test_setup_kata_run():
    # Given: A configured kata instance
    kata = SetupKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid koan response
    assert result.data is not None
    assert isinstance(result.data, Koan)
    assert result.data.koan is not None
    assert result.data.master is not None
    assert len(result.data.koan) > 0
    assert len(result.data.master) > 0

    # Display the wisdom
    print(f"\nKoan: {result.data.koan}")
    print(f"- {result.data.master}")
