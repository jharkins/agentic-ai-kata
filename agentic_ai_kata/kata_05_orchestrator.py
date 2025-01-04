from typing import Any, Dict

from pydantic import BaseModel, Field

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import KataSettings


class WorkerTask(BaseModel):
    """A task assigned to a worker"""

    task_id: str = Field(description="ID of this task")
    description: str = Field(description="What the worker needs to do")
    dependencies: list[str] = Field(description="IDs of tasks this depends on")


class WorkerResult(BaseModel):
    """Result from a worker's task execution"""

    task_id: str = Field(description="ID of the completed task")
    result: str = Field(description="Result from the worker")
    status: str = Field(description="Status of the task (success/failure)")


class OrchestratorResult(BaseModel):
    """Overall result from the orchestrator"""

    tasks: list[WorkerTask] = Field(description="All tasks that were assigned")
    results: list[WorkerResult] = Field(description="Results from all workers")
    final_output: str = Field(description="The orchestrator's final output")


class OrchestratorKata(KataBase):
    """
    Kata 05: Orchestrator-Workers Pattern

    This kata demonstrates:
    1. How to use a central orchestrator to delegate tasks
    2. How to manage dependencies between tasks
    3. How to handle worker failures and retries
    """

    def __init__(self):
        self.settings = KataSettings()

    def run(self) -> Any:
        """Demonstrates the orchestrator-workers pattern"""
        # TODO: Implement orchestrator-workers pattern
        raise NotImplementedError("This kata is not yet implemented")

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validates that the orchestrator pattern worked correctly"""
        # Check we have a valid result object
        if not result or not isinstance(result.data, OrchestratorResult):
            return False

        # Check we have tasks and results
        if not result.data.tasks or len(result.data.tasks) == 0:
            return False
        if not result.data.results or len(result.data.results) == 0:
            return False

        # Check each task
        task_ids = set()
        for task in result.data.tasks:
            if not isinstance(task, WorkerTask):
                return False
            if not task.task_id or len(task.task_id) == 0:
                return False
            task_ids.add(task.task_id)
            if not task.description or len(task.description) == 0:
                return False
            # Dependencies should reference valid task IDs
            if task.dependencies:
                if not all(dep in task_ids for dep in task.dependencies):
                    return False

        # Check each result
        for res in result.data.results:
            if not isinstance(res, WorkerResult):
                return False
            if not res.task_id or res.task_id not in task_ids:
                return False
            if not res.result or len(res.result) == 0:
                return False
            if not res.status or res.status not in ["success", "failure"]:
                return False

        # Check final output
        if not result.data.final_output or len(result.data.final_output) == 0:
            return False

        return True
