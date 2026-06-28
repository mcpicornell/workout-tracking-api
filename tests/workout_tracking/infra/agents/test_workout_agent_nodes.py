import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import date

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from workout_tracking.infra.agents.workout_agent_nodes import WorkoutAgentNodes
from workout_tracking.infra.agents.workout_agent_types import (
    WorkoutState,
    PreparedWorkoutData,
    ExerciseData,
    WorkoutExtraction,
    ExtractedExercise
)

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    # Mock with_structured_output to return a mock runnable
    mock_structured_llm = AsyncMock()
    llm.with_structured_output.return_value = mock_structured_llm
    return llm, mock_structured_llm

@pytest.fixture
def mock_exercise_repo():
    repo = AsyncMock()
    repo.get_all_exercises.return_value = [
        MagicMock(id=UUID(int=1), name="Bench Press", description="Chest exercise"),
        MagicMock(id=UUID(int=2), name="Squat", description="Leg exercise"),
    ]
    return repo

@pytest.fixture
def mock_user_exercise_repo():
    return AsyncMock()

@pytest.fixture
def nodes(mock_llm, mock_exercise_repo, mock_user_exercise_repo):
    llm, _ = mock_llm
    return WorkoutAgentNodes(
        llm=llm,
        exercise_repository=mock_exercise_repo,
        user_exercise_repository=mock_user_exercise_repo
    )

@pytest.mark.asyncio
async def test_prepare_workout_node_success(nodes, mock_llm):
    _, mock_structured_llm = mock_llm
    
    # Mock LLM output
    mock_structured_llm.ainvoke.return_value = WorkoutExtraction(
        exercises=[
            ExtractedExercise(name="Bench Press", sets=3, reps=10, weight=80),
            ExtractedExercise(name="Squat", sets=3, reps=8, weight=100),
        ]
    )

    state: WorkoutState = {
        "messages": [HumanMessage(content="I did 3 sets of 10 bench press at 80kg and 3 sets of 8 squats at 100kg")],
        "prepared_workout": None,
        "confirmation_status": None,
    }
    config = {"configurable": {"actor_id": str(uuid4())}}

    result = await nodes.prepare_workout_node(state, config)

    assert result["confirmation_status"] == "pending"
    assert isinstance(result["prepared_workout"], PreparedWorkoutData)
    assert len(result["prepared_workout"].exercises) == 2
    assert result["prepared_workout"].exercises[0].exercise_name == "Bench Press"
    assert result["prepared_workout"].exercises[0].weight == 80
    assert len(result["messages"]) == 2
    assert "Please confirm or reject" in result["messages"][-1].content

@pytest.mark.asyncio
async def test_confirm_workout_node_confirmed(nodes, mock_user_exercise_repo):
    user_id = uuid4()
    prepared_workout = PreparedWorkoutData(
        user_id=user_id,
        exercises=[ExerciseData(exercise_name="Bench Press", sets=3, reps=10, weight=80)],
        workout_date=date.today()
    )
    
    state: WorkoutState = {
        "messages": [HumanMessage(content="Yes, please confirm")],
        "prepared_workout": prepared_workout,
        "confirmation_status": "pending",
    }
    config = {"configurable": {"thread_id": str(uuid4())}}

    # Mock the internal _find_exercise_id to return a valid UUID
    nodes._find_exercise_id = AsyncMock(return_value=UUID(int=1))

    result = await nodes.confirm_workout_node(state, config)

    assert result["confirmation_status"] == "confirmed"
    assert result["prepared_workout"] is None
    assert "Workout saved successfully" in result["messages"][-1].content
    mock_user_exercise_repo.create_user_exercise.assert_called()


@pytest.mark.asyncio
async def test_confirm_workout_node_rejected(nodes):
    prepared_workout = PreparedWorkoutData(
        user_id=uuid4(),
        exercises=[ExerciseData(exercise_name="Bench Press", sets=3, reps=10, weight=80)],
        workout_date=date.today()
    )
    
    state: WorkoutState = {
        "messages": [HumanMessage(content="No, reject it")],
        "prepared_workout": prepared_workout,
        "confirmation_status": "pending",
    }
    config = {"configurable": {"thread_id": str(uuid4())}}

    result = await nodes.confirm_workout_node(state, config)

    assert result["confirmation_status"] == "rejected"
    assert result["prepared_workout"] is None
    assert "Workout data discarded" in result["messages"][-1].content
