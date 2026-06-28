import pytest
from unittest.mock import AsyncMock, MagicMock
from workout_tracking.adapters.workout_message_processor_adapter import WorkoutMessageProcessorAdapter
from workout_tracking.domain.workout_messages_use_cases_types import (
    ProcessWorkoutMessagePortInput,
    ProcessWorkoutMessagePortOutput,
)

@pytest.fixture
def mock_workout_agent():
    agent = MagicMock()
    agent.process_workout_message = AsyncMock()
    return agent

@pytest.fixture
def adapter(mock_workout_agent):
    return WorkoutMessageProcessorAdapter(mock_workout_agent)

@pytest.mark.asyncio
async def test_process_workout_message_success(adapter, mock_workout_agent):
    # Arrange
    input_data = ProcessWorkoutMessagePortInput(
        message="test message",
        user_id="user-123",
        job_id="job-123",
        workout_date="2026-06-28"
    )
    
    # We need to mock the mapper output too. 
    # Since the adapter uses mappers, we should ensure the mock_workout_agent returns 
    # something that map_process_workout_message_infra_to_domain can handle.
    
    # For simplicity, let's mock the return value of the agent.
    # Looking at workout_message_processor_adapter_types.py would be better.
    
    mock_infra_output = MagicMock()
    mock_infra_output.content = "Workout processed"
    mock_workout_agent.process_workout_message.return_value = mock_infra_output
    
    # Act
    result = await adapter.process_workout_message(input_data)
    
    # Assert
    assert result is not None
    mock_workout_agent.process_workout_message.assert_called_once()
