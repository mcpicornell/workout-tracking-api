import pytest
from workout_tracking.infra.repositories.exercise_repository import ExerciseRepository
from workout_tracking.infra.repositories.exercise_repository_types import ExerciseCreateInput, ExerciseUpdateInput

@pytest.mark.asyncio
async def test_create_exercise(db_session):
    repo = ExerciseRepository(db_session)
    ex_in = ExerciseCreateInput(name="Push-up", description="Basic bodyweight exercise")
    
    exercise = await repo.create(ex_in)
    
    assert exercise.name == "Push-up"
    assert exercise.id is not None

@pytest.mark.asyncio
async def test_get_exercise(db_session):
    repo = ExerciseRepository(db_session)
    ex_in = ExerciseCreateInput(name="Squat")
    created = await repo.create(ex_in)
    
    fetched = await repo.get_by_id(str(created.id))
    
    assert fetched is not None
    assert fetched.name == "Squat"

@pytest.mark.asyncio
async def test_update_exercise(db_session):
    repo = ExerciseRepository(db_session)
    ex_in = ExerciseCreateInput(name="Squat")
    created = await repo.create(ex_in)
    
    update_in = ExerciseUpdateInput(description="Leg day focus")
    updated = await repo.update(str(created.id), update_in)
    
    assert updated is not None
    assert updated.description == "Leg day focus"

@pytest.mark.asyncio
async def test_delete_exercise(db_session):
    repo = ExerciseRepository(db_session)
    ex_in = ExerciseCreateInput(name="Squat")
    created = await repo.create(ex_in)
    
    success = await repo.delete(str(created.id))
    
    assert success is True
    fetched = await repo.get_by_id(str(created.id))
    assert fetched is None
