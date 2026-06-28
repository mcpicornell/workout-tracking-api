from typing import Protocol

from .jobs_use_cases_types import (
    CreateJobInput,
    CreateJobOutput,
    CreateJobPortInput,
    GetJobByIdInput,
    GetJobByIdOutput,
    GetJobByIdPortInput,
    JobStoragePort,
    UpdateJobPortInput,
)


class JobsUseCases(Protocol):
    async def get_job_by_id(self, input: GetJobByIdInput) -> GetJobByIdOutput: ...
    async def create_job(self, input: CreateJobPortInput) -> None: ...
    async def update_job(self, input: UpdateJobPortInput) -> None: ...


class DefaultJobsUseCases(JobsUseCases):
    def __init__(self, job_storage_port: JobStoragePort):
        self._job_storage_port = job_storage_port

    async def get_job_by_id(self, input: GetJobByIdInput) -> GetJobByIdOutput:
        return await self._job_storage_port.get_job_by_id(
            GetJobByIdPortInput(job_id=input.job_id)
        )

    async def create_job(self, input: CreateJobInput) -> CreateJobOutput:
        return await self._job_storage_port.create_job(
            CreateJobPortInput(
                description=input.description,
                status=input.status,
            )
        )

    async def update_job(self, input: UpdateJobPortInput) -> None:
        await self._job_storage_port.update_job(
            UpdateJobPortInput(job_id=input.job_id, status=input.status)
        )
