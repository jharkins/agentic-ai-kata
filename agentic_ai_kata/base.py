from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel


class KataBase(ABC):
    """Base class for all katas"""

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Run the kata"""
        pass

    def cleanup(self) -> None:
        """Optional cleanup after kata execution"""
        pass


class AgentState(BaseModel):
    """Track agent state across steps"""

    memory: Dict[str, Any] = {}
    current_step: int = 0
    last_action: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
