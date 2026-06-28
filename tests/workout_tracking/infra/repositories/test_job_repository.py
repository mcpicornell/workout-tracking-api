from uuid import uuid4

import pytest

from workout_tracking.infra.db.models import JobModel, JobStatus
from workout_tracking.infra.repositories.job_repository import (
    DefaultJobRepository,
    JobRepository,
)
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobInput,
    DeleteJobInput,
    GetJobByIdInput,
    UpdateJobInput,
)


@pytest.mark.asyncio
async def test_create_job(db_session):
    repo = DefaultJobRepository(db_session)
    job_in = CreateJobInput(description="New Job")

    job = await repo.create_job(job_in)

    assert job.description == "New Job"
    assert job.id is not None
    assert job.status == JobStatus.PENDING


@pytest.mark.asyncio
async def test_get_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), description="Test Job", status=JobStatus.PENDING)
    db_session.add(job)
    await db_session.commit()

    fetched = await repo.get_job_by_id(GetJobByIdInput(id=job.id))

    assert fetched is not None
    assert fetched.description == "Test Job"


@pytest.mark.asyncio
async def test_update_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), description="Test Job", status=JobStatus.PENDING)
    db_session.add(job)
    await db_session.commit()

    update_in = UpdateJobInput(id=job.id, status=JobStatus.COMPLETED, result="Success")
    updated = await repo.update_job(update_in)

    assert updated is not None
    assert updated.status == JobStatus.COMPLETED
    assert updated.result == "Success"


@pytest.mark.asyncio
async def test_delete_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), description="Test Job", status=JobStatus.PENDING)
    db_session.add(job)
    await db_session.commit()

    success = await repo.delete_job(DeleteJobInput(id=job.id))

    assert success is True
    fetched = await repo.get_job_by_id(GetJobByIdInput(id=job.id))
    assert fetched is None
