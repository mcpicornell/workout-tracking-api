from dataclasses import asdict
from typing import List, Optional, Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db.models import ExerciseModel
from ..infra_exceptions import GenericInfraException
from .exercise_repository_types import (
    CreateExerciseInput,
    DeleteExerciseInput,
    ExerciseCreateOutput,
    ExerciseDB,
    ExerciseUpdateOutput,
    GetAllExercisesOutput,
    GetExerciseByIdInput,
    GetExerciseByJobIdInput,
    UpdateExerciseInput,
)


class ExerciseRepository(Protocol):
    async def get_exercise_by_id(
        self, input: GetExerciseByIdInput
    ) -> Optional[ExerciseDB]: ...
    async def create_exercise(
        self, input: CreateExerciseInput
    ) -> ExerciseCreateOutput: ...
    async def update_exercise(
        self, input: UpdateExerciseInput
    ) -> ExerciseUpdateOutput: ...
    async def delete_exercise(self, input: DeleteExerciseInput) -> bool: ...
    async def get_exercises_by_job_id(
        self, input: GetExerciseByJobIdInput
    ) -> List[ExerciseDB]: ...
    async def get_all_exercises(self) -> GetAllExercisesOutput: ...


class DefaultExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._cache: List[ExerciseDB] | None = None

    async def get_all_exercises(self) -> GetAllExercisesOutput:
        if self._cache is not None:
            return self._cache

        try:
            result = await self.session.execute(select(ExerciseModel))
            exercises = result.scalars().all()
            self._cache = [self._map_to_exercise_db(ex) for ex in exercises]
            return self._cache
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while getting all exercises"
            ) from e

    def invalidate_cache(self):
        self._cache = None

    async def get_exercise_by_id(
        self, input: GetExerciseByIdInput
    ) -> Optional[ExerciseDB]:
        try:
            result = await self.session.get(ExerciseModel, input.id)
            if not result:
                return None
            return self._map_to_exercise_db(result)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while getting exercise by id"
            ) from e

    async def create_exercise(self, input: CreateExerciseInput) -> ExerciseCreateOutput:
        try:
            async with self.session.begin_nested():
                exercise = ExerciseModel(**asdict(input))
                self.session.add(exercise)
            await self.session.commit()
            await self.session.refresh(exercise)
            return self._map_to_exercise_db(exercise)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while creating exercise"
            ) from e

    async def update_exercise(self, input: UpdateExerciseInput) -> ExerciseUpdateOutput:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(
                    select(ExerciseModel).where(ExerciseModel.id == input.id)
                )
                exercise = result.scalar_one_or_none()
                if not exercise:
                    return None

                update_data = asdict(input)
                update_data.pop("id")

                for field, value in update_data.items():
                    if value is not None:
                        setattr(exercise, field, value)

            await self.session.commit()
            await self.session.refresh(exercise)
            return self._map_to_exercise_db(exercise)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while updating exercise"
            ) from e

    async def delete_exercise(self, input: DeleteExerciseInput) -> bool:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(
                    select(ExerciseModel).where(ExerciseModel.id == input.id)
                )
                exercise = result.scalar_one_or_none()
                if exercise:
                    await self.session.delete(exercise)
                    await self.session.commit()
                    return True
            return False
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while deleting exercise"
            ) from e

    async def get_exercises_by_job_id(
        self, input: GetExerciseByJobIdInput
    ) -> List[ExerciseDB]:
        try:
            result = await self.session.execute(
                select(ExerciseModel).where(ExerciseModel.job_id == input.job_id)
            )
            exercises = result.scalars().all()
            return [self._map_to_exercise_db(ex) for ex in exercises]
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in ExerciseRepository while getting exercises by job id"
            ) from e

    def _map_to_exercise_db(self, exercise: ExerciseModel) -> ExerciseDB:
        return ExerciseDB(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            created_at=exercise.created_at,
            updated_at=exercise.updated_at,
            job_id=exercise.job_id,
        )
