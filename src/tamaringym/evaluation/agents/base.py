"""Agent interface: an Agent runs inside the task container."""

from __future__ import annotations

from abc import ABC, abstractmethod

from tamaringym.evaluation.types import AgentFnArguments


class Agent(ABC):
    @abstractmethod
    def run(self, args: AgentFnArguments) -> None:
        """Execute the task inside the container identified by
        ``args.container_id``."""
