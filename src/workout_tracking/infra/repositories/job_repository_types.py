from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from ..db.models import JobStatus

@dataclass(frozen=True, slots=True)
class CreateJobInput:
    name: str
    job_id: UUID
    description: Optional[str] = None
    status: JobStatus = JobStatus.PENDING

@dataclass(frozen=True, slots=True)
class UpdateJobInput:
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[JobStatus] = None
    job_id: Optional[UUID] = None

@dataclass(frozen=True, slots=True)
class GetJobByIdInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class GetJobByJobIdInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class DeleteJobInput:
    id: UUID

@dataclass(frozen=True, slots=True)
class JobDB:
    id: UUID
    name: str
    description: Optional[str]
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    job_id: UUID

JobCreateOutput = JobDB
JobUpdateOutput = Optional[JobDB]
