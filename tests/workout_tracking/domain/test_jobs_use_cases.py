import pytest
from unittest.mock import AsyncMock, MagicMock
from workout_tracking.domain.jobs_use_cases import DefaultJobsUseCases
from workout_tracking.domain.jobs_use_cases_types import (
    CreateJobInput,
    GetJobByIdInput,
    UpdateJobInput,
)

@pytest.fixture
def mock_job_storage():
    storage = MagicMock()
    storage.get_job_by_id = AsyncMock()
    storage.create_job = AsyncMock()
    storage.update_job = AsyncMock()
    return storage

@pytest.fixture
def use_cases(mock_job_storage):
    return DefaultJobsUseCases(job_storage_port=mock_job_storage)

@pytest.mark.asyncio
async def test_get_job_by_id(use_cases, mock_job_storage):
    input_data = GetJobByIdInput(job_id="job-123")
    mock_job_storage.get_job_by_id.return_value = MagicMock(id="job-123", status="PENDING")
    
    result = await use_cases.get_job_by_id(input_data)
    
    assert result.id == "job-123"
    mock_job_storage.get_job_by_id.assert_called_once()

@pytest.mark.asyncio
async def test_create_job(use_cases, mock_job_storage):
    input_data = CreateJobInput(description="Test Job", status="PENDING")
    
    await use_cases.create_job(input_data)
    
    mock_job_storage.create_job.assert_called_once()

@pytest.mark.asyncio
async def test_update_job(use_cases, mock_job_storage):
    input_data = UpdateJobInput(id="job-123", status="COMPLETED", result="Success")
    
    await use_cases.update_job(input_data)
    
    mock_job_storage.update_job.assert_called_once()
