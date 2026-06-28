from dataclasses import asdict
from typing import List, Optional, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import UserExerciseModel
from .user_exercise_repository_types import (
    CreateUserExerciseInput,
    UpdateUserExerciseInput,
    GetUserExerciseByIdInput,
    GetUserExerciseByJobIdInput,
    DeleteUserExerciseInput,
    UserExerciseDB,
    UserExerciseCreateOutput,
    UserExerciseUpdateOutput,
)
from ..infra_exceptions import GenericInfraException

class UserExerciseRepository(Protocol):
    async def get_user_exercise_by_id(self, input: GetUserExerciseByIdInput) -> Optional[UserExerciseDB]: ...
    async def create_user_exercise(self, input: CreateUserExerciseInput) -> UserExerciseCreateOutput: ...
    async def update_user_exercise(self, input: UpdateUserExerciseInput) -> UserExerciseUpdateOutput: ...
    async def delete_user_exercise(self, input: DeleteUserExerciseInput) -> bool: ...
    async def get_user_exercises_by_job_id(self, input: GetUserExerciseByJobIdInput) -> List[UserExerciseDB]: ...

class DefaultUserExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_exercise_by_id(self, input: GetUserExerciseByIdInput) -> Optional[UserExerciseDB]:
        try:
            item = await self.session.get(UserExerciseModel, input.id)
            if not item:
                return None
            return self._map_to_user_exercise_db(item)
        except Exception as e:
            raise GenericInfraException("An error occurred in UserExerciseRepository while getting user exercise by id") from e

    async def create_user_exercise(self, input: CreateUserExerciseInput) -> UserExerciseCreateOutput:
        try:
            async with self.session.begin_nested():
                item = UserExerciseModel(**asdict(input))
                self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
            return self._map_to_user_exercise_db(item)
        except Exception as e:
            raise GenericInfraException("An error occurred in UserExerciseRepository while creating user exercise") from e

    async def update_user_exercise(self, input: UpdateUserExerciseInput) -> UserExerciseUpdateOutput:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(UserExerciseModel).where(UserExerciseModel.id == input.id))
                item = result.scalar_one_or_none()
                if not item:
                    return None
                
                update_data = asdict(input)
                update_data.pop("id")
                
                for field, value in update_data.items():
                    if value is not None:
                        setattr(item, field, value)
            
            await self.session.commit()
            await self.session.refresh(item)
            return self._map_to_user_exercise_db(item)
        except Exception as e:
            raise GenericInfraException("An error occurred in UserExerciseRepository while updating user exercise") from e

    async def delete_user_exercise(self, input: DeleteUserExerciseInput) -> bool:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(UserExerciseModel).where(UserExerciseModel.id == input.id))
                item = result.scalar_one_or_none()
                if item:
                    await self.session.delete(item)
                    await self.session.commit()
                    return True
            return False
        except Exception as e:
            raise GenericInfraException("An error occurred in UserExerciseRepository while deleting user exercise") from e

    async def get_user_exercises_by_job_id(self, input: GetUserExerciseByJobIdInput) -> List[UserExerciseDB]:
        try:
            result = await self.session.execute(select(UserExerciseModel).where(UserExerciseModel.job_id == input.job_id))
            items = result.scalars().all()
            return [self._map_to_user_exercise_db(item) for item in items]
        except Exception as e:
            raise GenericInfraException("An error occurred in UserExerciseRepository while getting user exercises by job id") from e

    def _map_to_user_exercise_db(self, item: UserExerciseModel) -> UserExerciseDB:
        return UserExerciseDB(
            id=item.id,
            user_id=item.user_id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            weight=item.weight,
            date=item.date,
            created_at=item.created_at,
            updated_at=item.updated_at,
            job_id=item.job_id
        )
