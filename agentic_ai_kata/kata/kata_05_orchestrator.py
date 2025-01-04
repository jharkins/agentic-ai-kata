from typing import Any

from pydantic import BaseModel, Field

from ..base import KataBase
from ..settings import KataSettings


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
