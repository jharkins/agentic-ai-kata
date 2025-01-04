import pytest
from agentic_ai_kata.kata_04_parallel import ParallelKata, VotingResult, ParallelResult


def test_parallel_kata_initialization():
    # Given: A new kata instance
    kata = ParallelKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


def test_parallel_kata_run():
    # Given: A configured kata instance
    kata = ParallelKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid voting result
    assert result.data is not None
    assert isinstance(result.data, VotingResult)
    assert len(result.data.parallel_results) > 0
    assert result.data.winning_result is not None
    assert 0 <= result.data.vote_confidence <= 1

    # Display the parallel results and voting outcome
    print("\nParallel Results:")
    for pr in result.data.parallel_results:
        assert isinstance(pr, ParallelResult)
        print(f"\nTask {pr.task_id}:")
        print(f"Result: {pr.result}")
        print(f"Confidence: {pr.confidence:.2f}")

    print(f"\nWinning Result: {result.data.winning_result}")
    print(f"Vote Confidence: {result.data.vote_confidence:.2f}")
