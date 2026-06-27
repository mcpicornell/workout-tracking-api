from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass
class ExerciseCreateInput:
    name: str
    description: Optional[str] = None

@dataclass
class ExerciseUpdateInput:
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ExerciseDB:
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

ExerciseCreateOutput = ExerciseDB
ExerciseUpdateOutput = Optional[ExerciseDB]
