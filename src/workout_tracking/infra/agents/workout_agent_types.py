from dataclasses import dataclass
from datetime import date
from typing import Annotated, TypedDict
from uuid import UUID

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class ExtractedExercise(BaseModel):
    name: str = Field(description="The exact name of the exercise from the provided list")
    sets: int = Field(default=3, description="Number of sets")
    reps: int = Field(default=10, description="Number of repetitions")
    weight: int = Field(default=0, description="Weight used in kilograms")

class WorkoutExtraction(BaseModel):
    exercises: list[ExtractedExercise] = Field(description="List of exercises extracted from the message")

@dataclass(frozen=True, slots=True)
class LLMSettings:
    name: str
    api_key: str


@dataclass(frozen=True, slots=True)
class ProcessWorkoutMessageInput:
    user_id: UUID
    job_id: UUID
    message: str
    workout_date: date


@dataclass(frozen=True, slots=True)
class ProcessWorkoutMessageOutput:
    content: str


@dataclass(frozen=True, slots=True)
class ExerciseData:
    exercise_name: str
    sets: int
    reps: int
    weight: int


@dataclass(frozen=True, slots=True)
class WorkoutInput:
    user_id: UUID
    message: str
    workout_date: date


@dataclass(frozen=True, slots=True)
class PreparedWorkoutData:
    user_id: UUID
    exercises: list[ExerciseData]
    workout_date: date


@dataclass(frozen=True, slots=True)
class ConfirmWorkoutInput:
    prepared_data: PreparedWorkoutData
    confirmed: bool


class WorkoutState(TypedDict):
    messages: Annotated[list, add_messages]
    prepared_workout: PreparedWorkoutData | None
    confirmation_status: str | None
