import pytest
from agentic_ai_kata.kata_01_augmented import AugmentedKata, AugmentedResult
from agentic_ai_kata.settings import settings


def test_augmented_kata_initialization():
    # Then: It should have a valid API key
    assert settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_augmented_kata_run():
    # Given: A configured kata instance
    kata = AugmentedKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid augmented result
    assert kata.validate_result(result)
