from dataclasses import asdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from ..db.models import UserExerciseModel
from .user_exercise_repository_types import UserExerciseCreateInput, UserExerciseUpdateInput, UserExerciseDB, UserExerciseCreateOutput, UserExerciseUpdateOutput

class UserExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> Optional[UserExerciseDB]:
        result = await self.session.execute(select(UserExerciseModel).filter(UserExerciseModel.id == id))
        item = result.scalar_one_or_none()
        if not item:
            return None
        return UserExerciseDB(
            id=item.id,
            user_id=item.user_id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            weight=item.weight,
            date=item.date,
            created_at=item.created_at,
            updated_at=item.updated_at
        )

    async def create(self, in_data: UserExerciseCreateInput) -> UserExerciseCreateOutput:
        async with self.session.begin_nested():
            item = UserExerciseModel(**asdict(in_data))
            self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return UserExerciseDB(
            id=item.id,
            user_id=item.user_id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            weight=item.weight,
            date=item.date,
            created_at=item.created_at,
            updated_at=item.updated_at
        )

    async def update(self, id: str, in_data: UserExerciseUpdateInput) -> UserExerciseUpdateOutput:
        async with self.session.begin_nested():
            result = await self.session.execute(select(UserExerciseModel).filter(UserExerciseModel.id == id))
            item = result.scalar_one_or_none()
            if not item:
                return None
            
            update_data = asdict(in_data)
            for field, value in update_data.items():
                if value is not None:
                    setattr(item, field, value)
        
        await self.session.commit()
        await self.session.refresh(item)
        return UserExerciseDB(
            id=item.id,
            user_id=item.user_id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            weight=item.weight,
            date=item.date,
            created_at=item.created_at,
            updated_at=item.updated_at
        )

    async def delete(self, id: str) -> bool:
        async with self.session.begin_nested():
            result = await self.session.execute(select(UserExerciseModel).filter(UserExerciseModel.id == id))
            item = result.scalar_one_or_none()
            if item:
                await self.session.delete(item)
        await self.session.commit()
        return True

