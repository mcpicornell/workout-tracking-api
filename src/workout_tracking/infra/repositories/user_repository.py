from dataclasses import asdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from ..db.models import UserModel
from .user_repository_types import UserCreateInput, UserUpdateInput, UserDB, UserCreateOutput, UserUpdateOutput

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> Optional[UserDB]:
        result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserDB(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at
        )

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreateInput) -> UserCreateOutput:
        async with self.session.begin_nested():
            user = UserModel(email=user_in.email, hashed_password=user_in.password)
            self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserDB(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at
        )

    async def update(self, user_id: str, user_in: UserUpdateInput) -> UserUpdateOutput:
        async with self.session.begin_nested():
            result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                return None
            
            update_data = asdict(user_in)
            for field, value in update_data.items():
                if value is not None:
                    setattr(user, field, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        return UserDB(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at
        )

    async def delete(self, user_id: str) -> bool:
        async with self.session.begin_nested():
            result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                await self.session.delete(user)
                return True
        await self.session.commit()
        return False
