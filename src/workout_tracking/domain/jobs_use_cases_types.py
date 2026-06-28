from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID


class JobStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(frozen=True, slots=True)
class UpdateJobPortInput:
    id: UUID
    status: JobStatus
    result: str


@dataclass(frozen=True, slots=True)
class UpdateJobInput:
    id: UUID
    status: JobStatus
    result: str


@dataclass(frozen=True, slots=True)
class GetJobByIdPortInput:
    job_id: UUID


@dataclass(frozen=True, slots=True)
class GetJobByIdPortOutput:
    job_id: UUID


@dataclass(frozen=True, slots=True)
class GetJobByIdInput:
    job_id: UUID


@dataclass(frozen=True, slots=True)
class CreateJobInput:
    description: str
    status: JobStatus


@dataclass(frozen=True, slots=True)
class CreateJobPortInput:
    description: str
    status: JobStatus = JobStatus.PENDING


@dataclass(frozen=True, slots=True)
class DeleteJobPortInput:
    job_id: UUID


@dataclass(frozen=True, slots=True)
class Job:
    id: UUID
    description: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    result: str | None = None


type CreateJobOutput = Job
type GetJobByIdOutput = Job | None
type GetJobByIdPortOutput = Job | None
type CreateJobPortOutput = Job
type UpdateJobPortOutput = Job


class JobStoragePort(Protocol):
    async def create_job(self, input: CreateJobPortInput) -> CreateJobPortOutput: ...
    async def update_job(self, input: UpdateJobPortInput) -> UpdateJobPortOutput: ...
    async def get_job_by_id(
        self, input: GetJobByIdPortInput
    ) -> GetJobByIdPortOutput: ...
    async def delete_job(self, input: DeleteJobPortInput) -> bool: ...
