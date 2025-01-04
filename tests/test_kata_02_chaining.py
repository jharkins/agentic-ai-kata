import pytest
from agentic_ai_kata.kata_02_chaining import ChainingKata, ChainResult, ChainStep


def test_chaining_kata_initialization():
    # Given: A new kata instance
    kata = ChainingKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


def test_chaining_kata_run():
    # Given: A configured kata instance
    kata = ChainingKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid chain result
    assert result.data is not None
    assert isinstance(result.data, ChainResult)
    assert len(result.data.steps) > 0
    assert result.data.final_result is not None

    # Display the chain of thought
    print("\nChain of Thought:")
    for step in result.data.steps:
        assert isinstance(step, ChainStep)
        print(f"\nStep: {step.prompt}")
        print(f"Response: {step.response}")
        if step.next_step:
            print(f"Next: {step.next_step}")

    print(f"\nFinal Result: {result.data.final_result}")
