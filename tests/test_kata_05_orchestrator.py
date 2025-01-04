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


def test_orchestrator_kata_run():
    # Given: A configured kata instance
    kata = OrchestratorKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid orchestrator result
    assert result.data is not None
    assert isinstance(result.data, OrchestratorResult)
    assert len(result.data.tasks) > 0
    assert len(result.data.results) > 0
    assert result.data.final_output is not None

    # Display the orchestration process
    print("\nTask Assignments:")
    for task in result.data.tasks:
        assert isinstance(task, WorkerTask)
        print(f"\nTask {task.task_id}:")
        print(f"Description: {task.description}")
        if task.dependencies:
            print(f"Dependencies: {', '.join(task.dependencies)}")

    print("\nWorker Results:")
    for res in result.data.results:
        assert isinstance(res, WorkerResult)
        print(f"\nTask {res.task_id}:")
        print(f"Status: {res.status}")
        print(f"Result: {res.result}")

    print(f"\nFinal Output: {result.data.final_output}")
