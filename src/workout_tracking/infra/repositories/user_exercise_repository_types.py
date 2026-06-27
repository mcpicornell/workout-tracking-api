from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime, date

@dataclass
class UserExerciseCreateInput:
    user_id: UUID
    exercise_id: UUID
    sets: int
    reps: int
    weight: int
    date: date

@dataclass
class UserExerciseUpdateInput:
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None

@dataclass
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

UserExerciseCreateOutput = UserExerciseDB
UserExerciseUpdateOutput = Optional[UserExerciseDB]
