import pytest
from agentic_ai_kata.kata_07_agent import AgentKata, AgentResult, AgentThought


def test_agent_kata_initialization():
    # Given: A new kata instance
    kata = AgentKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_agent_kata_run():
    # Given: A configured kata instance
    kata = AgentKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid agent result
    assert result.data is not None
    assert isinstance(result.data, AgentResult)
    assert len(result.data.thoughts) > 0
    assert result.data.final_answer is not None
    assert len(result.data.tools_used) > 0

    # Display the agent's thought process
    print("\nAgent's Thought Process:")
    for thought in result.data.thoughts:
        assert isinstance(thought, AgentThought)
        print(f"\nThought: {thought.thought}")
        print(f"Action: {thought.action}")
        print(f"Observation: {thought.observation}")

    print(f"\nTools Used: {', '.join(result.data.tools_used)}")
    print(f"Final Answer: {result.data.final_answer}")
