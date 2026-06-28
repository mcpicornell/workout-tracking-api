from dataclasses import asdict
from typing import Optional, Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from workout_tracking.infra.db.models import JobModel
from workout_tracking.infra.infra_exceptions import GenericInfraException
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobInput,
    CreateJobOutput,
    DeleteJobInput,
    GetJobByIdInput,
    JobDB,
    UpdateJobInput,
    UpdateJobOutput,
)


class JobRepository(Protocol):
    async def get_job_by_id(self, input: GetJobByIdInput) -> Optional[JobDB]: ...
    async def create_job(self, input: CreateJobInput) -> CreateJobOutput: ...
    async def update_job(self, input: UpdateJobInput) -> UpdateJobOutput: ...
    async def delete_job(self, input: DeleteJobInput) -> bool: ...


class DefaultJobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_job_by_id(self, input: GetJobByIdInput) -> Optional[JobDB]:
        try:
            job = await self.session.get(JobModel, input.id)
            if not job:
                return None
            return self._map_to_job_db(job)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in JobRepository while getting job by id"
            ) from e

    async def create_job(self, input: CreateJobInput) -> CreateJobOutput:
        try:
            async with self.session.begin_nested():
                job = JobModel(**asdict(input))
                self.session.add(job)
            await self.session.commit()
            await self.session.refresh(job)
            return self._map_to_job_db(job)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in JobRepository while creating job"
            ) from e

    async def update_job(self, input: UpdateJobInput) -> UpdateJobOutput:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(
                    select(JobModel).where(JobModel.id == input.id)
                )
                job = result.scalar_one_or_none()
                if not job:
                    return None

                update_data = asdict(input)
                update_data.pop("id")

                for field, value in update_data.items():
                    if value is not None:
                        setattr(job, field, value)

            await self.session.commit()
            await self.session.refresh(job)
            return self._map_to_job_db(job)
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in JobRepository while updating job"
            ) from e

    async def delete_job(self, input: DeleteJobInput) -> bool:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(
                    select(JobModel).where(JobModel.id == input.id)
                )
                job = result.scalar_one_or_none()
                if job:
                    await self.session.delete(job)
                    await self.session.commit()
                    return True
            return False
        except Exception as e:
            raise GenericInfraException(
                "An error occurred in JobRepository while deleting job"
            ) from e

    def _map_to_job_db(self, job: JobModel) -> JobDB:
        return JobDB(
            id=job.id,
            description=job.description,
            status=job.status,
            result=job.result,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
