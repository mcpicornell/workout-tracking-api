from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime, date

@dataclass(frozen=True, slots=True)
class CreateUserExerciseInput:
    user_id: UUID
    exercise_id: UUID
    sets: int
    reps: int
    weight: int
    date: date
    job_id: UUID

@dataclass(frozen=True, slots=True)
class UpdateUserExerciseInput:
    id: UUID
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None
    job_id: Optional[UUID] = None

@dataclass(frozen=True, slots=True)
class GetUserExerciseByIdInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class GetUserExerciseByJobIdInput:
    job_id: UUID

@dataclass(frozen=True, slots=True)
class DeleteUserExerciseInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class UserExerciseDB:
    id: UUID
    user_id: UUID
    exercise_id: UUID
    sets: int
    reps: int
    weight: int
    date: date
    created_at: datetime
    updated_at: datetime
    job_id: UUID

UserExerciseCreateOutput = UserExerciseDB
UserExerciseUpdateOutput = Optional[UserExerciseDB]
