from dataclasses import asdict
from typing import List, Optional, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import UserModel
from .user_repository_types import (
    CreateUserInput,
    UpdateUserInput,
    GetUserByIdInput,
    GetUserByEmailInput,
    GetUserByJobIdInput,
    DeleteUserInput,
    UserDB,
    UserCreateOutput,
    UserUpdateOutput,
)
from ..infra_exceptions import GenericInfraException

class UserRepository(Protocol):
    async def get_user_by_id(self, input: GetUserByIdInput) -> Optional[UserDB]: ...
    async def get_user_by_email(self, input: GetUserByEmailInput) -> Optional[UserModel]: ...
    async def create_user(self, input: CreateUserInput) -> UserCreateOutput: ...
    async def update_user(self, input: UpdateUserInput) -> UserUpdateOutput: ...
    async def delete_user(self, input: DeleteUserInput) -> bool: ...
    async def get_users_by_job_id(self, input: GetUserByJobIdInput) -> List[UserDB]: ...

class DefaultUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, input: GetUserByIdInput) -> Optional[UserDB]:
        try:
            user = await self.session.get(UserModel, input.id)
            if not user:
                return None
            return self._map_to_user_db(user)
        except Exception as e:
            raise GenericInfraException(f"Error while getting user by id: {e}") from e

    async def get_user_by_email(self, input: GetUserByEmailInput) -> Optional[UserModel]:
        try:
            result = await self.session.execute(select(UserModel).where(UserModel.email == input.email))
            return result.scalar_one_or_none()
        except Exception as e:
            raise GenericInfraException(f"Error while getting user by email: {e}") from e

    async def create_user(self, input: CreateUserInput) -> UserCreateOutput:
        try:
            async with self.session.begin_nested():
                user = UserModel(email=input.email, hashed_password=input.password, job_id=input.job_id)
                self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return self._map_to_user_db(user)
        except Exception as e:
            raise GenericInfraException(f"Error while creating user: {e}") from e

    async def update_user(self, input: UpdateUserInput) -> UserUpdateOutput:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(UserModel).where(UserModel.id == input.id))
                user = result.scalar_one_or_none()
                if not user:
                    return None
                
                update_data = asdict(input)
                update_data.pop("id")
                
                for field, value in update_data.items():
                    if value is not None:
                        setattr(user, field, value)
            
            await self.session.commit()
            await self.session.refresh(user)
            return self._map_to_user_db(user)
        except Exception as e:
            raise GenericInfraException(f"Error while updating user: {e}") from e

    async def delete_user(self, input: DeleteUserInput) -> bool:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(UserModel).where(UserModel.id == input.id))
                user = result.scalar_one_or_none()
                if user:
                    await self.session.delete(user)
                    await self.session.commit()
                    return True
            return False
        except Exception as e:
            raise GenericInfraException(f"Error while deleting user: {e}") from e

    async def get_users_by_job_id(self, input: GetUserByJobIdInput) -> List[UserDB]:
        try:
            result = await self.session.execute(select(UserModel).where(UserModel.job_id == input.job_id))
            users = result.scalars().all()
            return [self._map_to_user_db(user) for user in users]
        except Exception as e:
            raise GenericInfraException(f"Error while getting users by job id: {e}") from e

    def _map_to_user_db(self, user: UserModel) -> UserDB:
        return UserDB(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            job_id=user.job_id
        )
