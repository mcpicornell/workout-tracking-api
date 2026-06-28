from dataclasses import asdict
from typing import List, Optional, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import JobModel
from .job_repository_types import (
    CreateJobInput,
    UpdateJobInput,
    GetJobByIdInput,
    GetJobByJobIdInput,
    DeleteJobInput,
    JobDB,
    JobCreateOutput,
    JobUpdateOutput,
)
from ..infra_exceptions import GenericInfraException

class JobRepository(Protocol):
    async def get_job_by_id(self, input: GetJobByIdInput) -> Optional[JobDB]: ...
    async def create_job(self, input: CreateJobInput) -> JobCreateOutput: ...
    async def update_job(self, input: UpdateJobInput) -> JobUpdateOutput: ...
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
            raise GenericInfraException("An error occurred in JobRepository while getting job by id") from e

    async def create_job(self, input: CreateJobInput) -> JobCreateOutput:
        try:
            async with self.session.begin_nested():
                job = JobModel(**asdict(input))
                self.session.add(job)
            await self.session.commit()
            await self.session.refresh(job)
            return self._map_to_job_db(job)
        except Exception as e:
            raise GenericInfraException("An error occurred in JobRepository while creating job") from e

    async def update_job(self, input: UpdateJobInput) -> JobUpdateOutput:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(JobModel).filter(JobModel.id == input.id))
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
            raise GenericInfraException("An error occurred in JobRepository while updating job") from e

    async def delete_job(self, input: DeleteJobInput) -> bool:
        try:
            async with self.session.begin_nested():
                result = await self.session.execute(select(JobModel).filter(JobModel.id == input.id))
                job = result.scalar_one_or_none()
                if job:
                    await self.session.delete(job)
                    await self.session.commit()
                    return True
            return False
        except Exception as e:
            raise GenericInfraException("An error occurred in JobRepository while deleting job") from e

    def _map_to_job_db(self, job: JobModel) -> JobDB:
        return JobDB(
            id=job.id,
            name=job.name,
            description=job.description,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
            job_id=job.job_id
        )
