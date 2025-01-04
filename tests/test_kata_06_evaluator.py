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


def test_evaluator_kata_run():
    # Given: A configured kata instance
    kata = EvaluatorKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid evaluator result
    assert result.data is not None
    assert isinstance(result.data, EvaluatorResult)
    assert len(result.data.attempts) > 0
    assert result.data.final_result is not None
    assert 0 <= result.data.final_score <= 1

    # Display the optimization process
    print("\nOptimization Process:")
    for attempt in result.data.attempts:
        assert isinstance(attempt, OptimizationAttempt)
        assert isinstance(attempt.evaluation, Evaluation)
        print(f"\nAttempt {attempt.attempt_number}:")
        print(f"Result: {attempt.result}")
        print(f"Score: {attempt.evaluation.score:.2f}")
        print(f"Feedback: {attempt.evaluation.feedback}")
        if attempt.evaluation.suggestions:
            print("Suggestions:")
            for suggestion in attempt.evaluation.suggestions:
                print(f"- {suggestion}")

    print(f"\nFinal Result: {result.data.final_result}")
    print(f"Final Score: {result.data.final_score:.2f}")
