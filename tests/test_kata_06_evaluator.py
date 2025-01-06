import pytest
from agentic_ai_kata.kata_06_evaluator import (
    EvaluatorKata,
    EvaluatorResult,
    OptimizationAttempt,
    Evaluation,
)


def test_evaluator_kata_initialization():
    # Given: A new kata instance
    kata = EvaluatorKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_evaluator_kata_run():
    # Given: A configured kata instance
    kata = EvaluatorKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid result
    assert kata.validate_result(result)
