import pytest
from uuid import uuid4
from workout_tracking.infra.repositories.job_repository import JobRepository, DefaultJobRepository
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobInput,
    UpdateJobInput,
    GetJobByIdInput,
    GetJobByJobIdInput,
    DeleteJobInput
)
from workout_tracking.infra.db.models import JobModel, JobStatus

@pytest.mark.asyncio
async def test_create_job(db_session):
    repo = DefaultJobRepository(db_session)
    job_in = CreateJobInput(name="New Job", job_id=uuid4())
    
    job = await repo.create_job(job_in)
    
    assert job.name == "New Job"
    assert job.id is not None
    assert job.job_id == job_in.job_id

@pytest.mark.asyncio
async def test_get_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), name="Test Job", description="Test Job Description", status=JobStatus.PENDING, job_id=uuid4())
    db_session.add(job)
    await db_session.commit()
    
    fetched = await repo.get_job_by_id(GetJobByIdInput(id=str(job.id)))
    
    assert fetched is not None
    assert fetched.name == "Test Job"

@pytest.mark.asyncio
async def test_update_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), name="Test Job", description="Test Job Description", status=JobStatus.PENDING, job_id=uuid4())
    db_session.add(job)
    await db_session.commit()
    
    update_in = UpdateJobInput(id=str(job.id), name="Updated Job")
    updated = await repo.update_job(update_in)
    
    assert updated is not None
    assert updated.name == "Updated Job"

@pytest.mark.asyncio
async def test_delete_job(db_session):
    repo = DefaultJobRepository(db_session)
    job = JobModel(id=uuid4(), name="Test Job", description="Test Job Description", status=JobStatus.PENDING, job_id=uuid4())
    db_session.add(job)
    await db_session.commit()
    
    success = await repo.delete_job(DeleteJobInput(id=str(job.id)))
    
    assert success is True
    fetched = await repo.get_job_by_id(GetJobByIdInput(id=str(job.id)))
    assert fetched is None
