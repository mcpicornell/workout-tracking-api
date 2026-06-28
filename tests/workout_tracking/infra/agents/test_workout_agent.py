import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import date

from langgraph.checkpoint.memory import MemorySaver
from workout_tracking.infra.agents.workout_agent import DefaultWorkoutAgent as WorkoutAgent
from workout_tracking.infra.agents.workout_agent_types import (
    LLMSettings,
    ProcessWorkoutMessageInput,
    WorkoutExtraction,
    ExtractedExercise
)

@pytest.fixture
def mock_exercise_repo():
    repo = AsyncMock()
    repo.get_all_exercises.return_value = [
        MagicMock(id=UUID(int=1), name="Bench Press", description="Chest"),
    ]
    return repo

@pytest.fixture
def mock_user_exercise_repo():
    return AsyncMock()

@pytest.fixture
def mock_settings():
    return LLMSettings(name="gemini-pro", api_key="fake_key")

@pytest.fixture
def agent(mock_exercise_repo, mock_user_exercise_repo, mock_settings):
    # We need to mock the LLM inside the agent
    # Since WorkoutAgent creates ChatGoogleGenerativeAI internally, 
    # we can patch it or mock the agent's internal _llm after init.
    checkpointer = MemorySaver()
    agent_instance = WorkoutAgent(
        exercise_repository=mock_exercise_repo,
        user_exercise_repository=mock_user_exercise_repo,
        checkpointer=checkpointer,
        settings=mock_settings,
    )
    
    # Mock the LLM that was created inside
    mock_llm = MagicMock()
    mock_structured_llm = AsyncMock()
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    # Inject the mock LLM into the agent and its nodes
    agent_instance._llm = mock_llm
    agent_instance._nodes._llm = mock_llm
    
    # Store the structured mock to configure it in tests
    agent_instance.mock_structured_llm = mock_structured_llm
    
    return agent_instance

    @pytest.mark.asyncio
    async def test_process_workout_message_flow(agent):
        # Configure the LLM mock for this test
        agent.mock_structured_llm.ainvoke.return_value = WorkoutExtraction(
            exercises=[ExtractedExercise(name="Bench Press", sets=3, reps=10, weight=80)]
        )
    
        input_data = ProcessWorkoutMessageInput(
            user_id=uuid4(),
            job_id=uuid4(),
            message="3x10 bench press 80kg",
            workout_date=date.today()
        )
    
        result = await agent.process_workout_message(input_data)
    
        assert result.content is not None
        # Check that it's a preparation message, not a success message
        assert "Prepared workout data" in result.content
        assert "confirm or reject" in result.content.lower()

    assert "Bench Press" in result.content

@pytest.mark.asyncio
async def test_confirm_workout_flow(agent):
    # This test is tricky because confirm_workout doesn't take the state, 
    # it just sends a message to the graph. 
    # We need to ensure the graph has a 'pending' state for a thread.
    
    # 1. First, prepare a workout for a specific thread
    thread_id = uuid4()
    user_id = uuid4()
    agent.mock_structured_llm.ainvoke.return_value = WorkoutExtraction(
        exercises=[ExtractedExercise(name="Bench Press", sets=3, reps=10, weight=80)]
    )
    
    await agent.process_workout_message(ProcessWorkoutMessageInput(
        user_id=user_id,
        job_id=thread_id,
        message="bench press",
        workout_date=date.today()
    ))
    
    # 2. Now confirm it
    result = await agent.confirm_workout(confirmed=True, job_id=thread_id, user_id=user_id)
    
    assert "Workout saved successfully" in result
