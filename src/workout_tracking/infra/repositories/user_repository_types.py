from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass(frozen=True, slots=True)
class CreateUserInput:
    email: str
    password: str
    job_id: UUID

@dataclass(frozen=True, slots=True)
class UpdateUserInput:
    id: UUID
    email: Optional[str] = None
    is_active: Optional[bool] = None
    job_id: Optional[UUID] = None

@dataclass(frozen=True, slots=True)
class GetUserByIdInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class GetUserByEmailInput:
    email: str

@dataclass(frozen=True, slots=True)
class GetUserByJobIdInput:
    job_id: UUID

@dataclass(frozen=True, slots=True)
class DeleteUserInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class UserDB:
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    job_id: UUID

UserCreateOutput = UserDB
UserUpdateOutput = Optional[UserDB]
