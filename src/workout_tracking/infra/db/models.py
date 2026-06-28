import uuid
from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

from .database import Base


def get_now_utc():
    return datetime.now(timezone.utc)


class GUID(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, _):
        return str(value) if value else None

    def process_result_value(self, value, _):
        return uuid.UUID(value) if value else None


class JobStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    description = Column(String)
    status = Column(
        SQLEnum(JobStatus),
        default=JobStatus.PENDING,
        nullable=False,
    )
    result = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_now_utc)
    updated_at = Column(DateTime, default=get_now_utc, onupdate=get_now_utc)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=get_now_utc)
    updated_at = Column(DateTime, default=get_now_utc, onupdate=get_now_utc)
    job_id = Column(GUID, ForeignKey("jobs.id"), nullable=True)

    user_exercises = relationship("UserExerciseModel", back_populates="user")


class ExerciseModel(Base):
    __tablename__ = "exercises"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_now_utc)
    updated_at = Column(DateTime, default=get_now_utc, onupdate=get_now_utc)
    job_id = Column(GUID, ForeignKey("jobs.id"), nullable=False)

    user_exercises = relationship("UserExerciseModel", back_populates="exercise")


class UserExerciseModel(Base):
    __tablename__ = "user_exercises"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(GUID, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Integer)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=get_now_utc)
    updated_at = Column(DateTime, default=get_now_utc, onupdate=get_now_utc)
    job_id = Column(GUID, ForeignKey("jobs.id"), nullable=False)

    exercise = relationship("ExerciseModel", back_populates="user_exercises")
    user = relationship("UserModel", back_populates="user_exercises")
