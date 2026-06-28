import pytest
from unittest.mock import AsyncMock, MagicMock
from workout_tracking.domain.workout_messages_use_cases import DefaultWorkoutMessagesUseCases
from workout_tracking.domain.workout_messages_use_cases_types import ProcessWorkoutMessageInput
from workout_tracking.domain.jobs_use_cases_types import JobStatus

@pytest.fixture
def mock_processor():
    processor = MagicMock()
    processor.process_workout_message = AsyncMock()
    return processor

@pytest.fixture
def mock_storage():
    storage = MagicMock()
    storage.update_job = AsyncMock()
    return storage

@pytest.fixture
def use_cases(mock_processor, mock_storage):
    return DefaultWorkoutMessagesUseCases(
        workout_message_processor_port=mock_processor,
        job_storage_port=mock_storage
    )

@pytest.mark.asyncio
async def test_process_workout_message_success(use_cases, mock_processor, mock_storage):
    input_data = ProcessWorkoutMessageInput(
        message="test",
        user_id="user-123",
        job_id="job-123"
    )
    
    mock_processor.process_workout_message.return_value = MagicMock(result="Success")
    
    await use_cases.process_workout_message(input_data)
    
    mock_processor.process_workout_message.assert_called_once()
    mock_storage.update_job.assert_called_once()
    # Check if status was set to COMPLETED
    args, _ = mock_storage.update_job.call_args
    assert args[0].status == JobStatus.COMPLETED

@pytest.mark.asyncio
async def test_process_workout_message_failure(use_cases, mock_processor, mock_storage):
    input_data = ProcessWorkoutMessageInput(
        message="test",
        user_id="user-123",
        job_id="job-123"
    )
    
    mock_processor.process_workout_message.side_effect = Exception("Error")
    
    with pytest.raises(Exception):
        await use_cases.process_workout_message(input_data)
    
    mock_storage.update_job.assert_called_once()
    # Check if status was set to FAILED
    args, _ = mock_storage.update_job.call_args
    assert args[0].status == JobStatus.FAILED
