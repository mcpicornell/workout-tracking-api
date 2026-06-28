from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ..db.models import JobStatus


@dataclass(frozen=True, slots=True)
class CreateJobInput:
    description: str
    status: JobStatus = JobStatus.PENDING


@dataclass(frozen=True, slots=True)
class UpdateJobInput:
    id: UUID
    status: JobStatus
    result: str


@dataclass(frozen=True, slots=True)
class GetJobByIdInput:
    id: UUID


@dataclass(frozen=True, slots=True)
class DeleteJobInput:
    id: UUID


@dataclass(frozen=True, slots=True)
class JobDB:
    id: UUID
    description: Optional[str]
    status: JobStatus
    result: Optional[str]
    created_at: datetime
    updated_at: datetime


CreateJobOutput = JobDB
UpdateJobOutput = Optional[JobDB]
GetJobByIdOutput = Optional[JobDB]
