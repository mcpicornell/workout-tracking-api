from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ProcessWorkoutMessageInput:
    message: str
    job_id: UUID


@dataclass(frozen=True, slots=True)
class ProcessWorkoutMessagePortInput:
    message: str


@dataclass(frozen=True, slots=True)
class ProcessWorkoutMessagePortOutput:
    result: str


class WorkoutMessageProcessorPort(Protocol):
    async def process_workout_message(
        self, input: ProcessWorkoutMessagePortInput
    ) -> ProcessWorkoutMessagePortOutput: ...
