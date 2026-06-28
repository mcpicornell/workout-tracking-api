from workout_tracking.domain.jobs_use_cases_types import (
    CreateJobOutput,
    CreateJobPortInput,
    DeleteJobPortInput,
    GetJobByIdPortInput,
    GetJobByIdPortOutput,
    JobStoragePort,
    UpdateJobPortInput,
    UpdateJobPortOutput,
)
from workout_tracking.infra.repositories.job_repository import JobRepository

from .jobs_storage_adapter_mappers import (
    map_domain_job_to_infra_create_input,
    map_domain_job_to_infra_delete_input,
    map_domain_job_to_infra_get_by_id_input,
    map_domain_job_to_infra_update_input,
    map_infra_job_output_to_domain,
)


class JobsStorageAdapter(JobStoragePort):
    def __init__(self, job_repository: JobRepository):
        self._job_repository = job_repository

    async def get_job_by_id(self, input: GetJobByIdPortInput) -> GetJobByIdPortOutput:
        output = await self._job_repository.get_job_by_id(
            map_domain_job_to_infra_get_by_id_input(input)
        )
        return map_infra_job_output_to_domain(output)

    async def create_job(self, input: CreateJobPortInput) -> CreateJobOutput:
        output = await self._job_repository.create_job(
            map_domain_job_to_infra_create_input(input)
        )
        return map_infra_job_output_to_domain(output)

    async def update_job(self, input: UpdateJobPortInput) -> UpdateJobPortOutput:
        output = await self._job_repository.update_job(
            map_domain_job_to_infra_update_input(input)
        )
        return map_infra_job_output_to_domain(output)

    async def delete_job(self, input: DeleteJobPortInput) -> bool:
        return await self._job_repository.delete_job(
            map_domain_job_to_infra_delete_input(input)
        )
