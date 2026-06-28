from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateExerciseInput:
    name: str
    job_id: UUID
    description: Optional[str] = None


@dataclass(frozen=True, slots=True)
class UpdateExerciseInput:
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    job_id: Optional[UUID] = None


@dataclass(frozen=True, slots=True)
class GetExerciseByIdInput:
    id: UUID


@dataclass(frozen=True, slots=True)
class GetExerciseByJobIdInput:
    job_id: UUID


@dataclass(frozen=True, slots=True)
class DeleteExerciseInput:
    id: UUID


@dataclass(frozen=True, slots=True)
class ExerciseDB:
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    job_id: UUID


ExerciseCreateOutput = ExerciseDB
ExerciseUpdateOutput = Optional[ExerciseDB]
GetAllExercisesOutput = List[ExerciseDB]
