import pytest
from agentic_ai_kata.kata_01_augmented import AugmentedKata, AugmentedResult


def test_augmented_kata_initialization():
    # Given: A new kata instance
    kata = AugmentedKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


def test_augmented_kata_run():
    # Given: A configured kata instance
    kata = AugmentedKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid augmented result
    assert kata.validate_result(result)
