from uuid import uuid4

import pytest

from workout_tracking.domain.jobs_use_cases_types import (
    CreateJobPortInput,
    DeleteJobPortInput,
    GetJobByIdPortInput,
    JobStatus,
    UpdateJobPortInput,
)
from workout_tracking.infra.repositories.job_repository import DefaultJobRepository
from workout_tracking.adapters.jobs_storage_adapter import JobsStorageAdapter
from workout_tracking.domain.domain_exceptions import NotFoundException


@pytest.mark.asyncio
async def test_adapter_get_job_by_id(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)

    # First create a job
    job_id = uuid4()

    # Simulate creating a job directly in DB for testing
    from workout_tracking.infra.db.models import JobModel

    job_model = JobModel(
        id=job_id,
        description="Test Job",
        status=JobStatus.PENDING,
    )
    db_session.add(job_model)
    await db_session.commit()

    # Test get_job_by_id
    input = GetJobByIdPortInput(job_id=job_id)
    result = await adapter.get_job_by_id(input)

    assert result is not None
    assert result.id == job_id
    assert result.description == "Test Job"
    assert result.status == JobStatus.PENDING


@pytest.mark.asyncio
async def test_adapter_get_job_by_id_not_found(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)
    
    input = GetJobByIdPortInput(job_id=uuid4())
    with pytest.raises(NotFoundException):
        await adapter.get_job_by_id(input)


@pytest.mark.asyncio
async def test_adapter_create_job(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)

    input = CreateJobPortInput(description="New Job", status=JobStatus.PENDING)
    result = await adapter.create_job(input)

    assert result is not None
    assert result.description == "New Job"
    assert result.status == JobStatus.PENDING
    assert result.id is not None


@pytest.mark.asyncio
async def test_adapter_update_job(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)

    # First create a job
    from workout_tracking.infra.db.models import JobModel

    job_id = uuid4()
    job_model = JobModel(
        id=job_id,
        description="Test Job",
        status=JobStatus.PENDING,
    )
    db_session.add(job_model)
    await db_session.commit()

    # Update the job
    input = UpdateJobPortInput(id=job_id, status=JobStatus.COMPLETED, result="Success")
    result = await adapter.update_job(input)

    assert result is not None
    assert result.id == job_id
    assert result.status == JobStatus.COMPLETED
    assert result.result == "Success"


@pytest.mark.asyncio
async def test_adapter_delete_job(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)

    # First create a job
    from workout_tracking.infra.db.models import JobModel

    job_id = uuid4()
    job_model = JobModel(
        id=job_id,
        description="Test Job",
        status=JobStatus.PENDING,
    )
    db_session.add(job_model)
    await db_session.commit()

    # Delete the job
    input = DeleteJobPortInput(job_id=job_id)
    result = await adapter.delete_job(input)

    assert result is True

    # Verify it's deleted
    get_input = GetJobByIdPortInput(job_id=job_id)
    with pytest.raises(NotFoundException):
        await adapter.get_job_by_id(get_input)


@pytest.mark.asyncio
async def test_adapter_delete_job_not_found(db_session):
    repo = DefaultJobRepository(db_session)
    adapter = JobsStorageAdapter(repo)

    input = DeleteJobPortInput(job_id=uuid4())
    result = await adapter.delete_job(input)

    assert result is False
