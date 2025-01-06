import pytest
from agentic_ai_kata.kata_05_orchestrator import (
    OrchestratorKata,
    OrchestratorResult,
    WorkerTask,
    WorkerResult,
)


def test_orchestrator_kata_initialization():
    # Given: A new kata instance
    kata = OrchestratorKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_orchestrator_kata_run():
    # Given: A configured kata instance
    kata = OrchestratorKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid result
    assert kata.validate_result(result)
