from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass
class UserCreateInput:
    email: str
    password: str

@dataclass
class UserUpdateInput:
    email: Optional[str] = None
    is_active: Optional[bool] = None

@dataclass
class UserDB:
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

UserCreateOutput = UserDB
UserUpdateOutput = Optional[UserDB]
