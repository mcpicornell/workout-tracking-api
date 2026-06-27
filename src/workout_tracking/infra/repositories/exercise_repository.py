from dataclasses import asdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from ..db.models import ExerciseModel
from .exercise_repository_types import ExerciseCreateInput, ExerciseUpdateInput, ExerciseDB, ExerciseCreateOutput, ExerciseUpdateOutput

class ExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, exercise_id: str) -> Optional[ExerciseDB]:
        result = await self.session.execute(select(ExerciseModel).filter(ExerciseModel.id == exercise_id))
        exercise = result.scalar_one_or_none()
        if not exercise:
            return None
        return ExerciseDB(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            created_at=exercise.created_at,
            updated_at=exercise.updated_at
        )

    async def create(self, exercise_in: ExerciseCreateInput) -> ExerciseCreateOutput:
        async with self.session.begin_nested():
            exercise = ExerciseModel(**asdict(exercise_in))
            self.session.add(exercise)
        await self.session.commit()
        await self.session.refresh(exercise)
        return ExerciseDB(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            created_at=exercise.created_at,
            updated_at=exercise.updated_at
        )

    async def update(self, exercise_id: str, exercise_in: ExerciseUpdateInput) -> ExerciseUpdateOutput:
        async with self.session.begin_nested():
            result = await self.session.execute(select(ExerciseModel).filter(ExerciseModel.id == exercise_id))
            exercise = result.scalar_one_or_none()
            if not exercise:
                return None
            
            update_data = asdict(exercise_in)
            for field, value in update_data.items():
                if value is not None:
                    setattr(exercise, field, value)
        
        await self.session.commit()
        await self.session.refresh(exercise)
        return ExerciseDB(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            created_at=exercise.created_at,
            updated_at=exercise.updated_at
        )

    async def delete(self, exercise_id: str) -> bool:
        async with self.session.begin_nested():
            result = await self.session.execute(select(ExerciseModel).filter(ExerciseModel.id == exercise_id))
            exercise = result.scalar_one_or_none()
            if exercise:
                await self.session.delete(exercise)
                await self.session.commit()
                return True
        return False
