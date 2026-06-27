import pytest
from datetime import date
from workout_tracking.infra.repositories.user_exercise_repository import UserExerciseRepository
from workout_tracking.infra.repositories.user_exercise_repository_types import UserExerciseCreateInput, UserExerciseUpdateInput
from workout_tracking.infra.db.models import UserModel, ExerciseModel
from uuid import uuid4

@pytest.fixture
async def setup_data(db_session):
    user = UserModel(id=uuid4(), email="user@test.com", hashed_password="pw")
    ex = ExerciseModel(id=uuid4(), name="Squat")
    db_session.add(user)
    db_session.add(ex)
    await db_session.commit()
    return user.id, ex.id

@pytest.mark.asyncio
async def test_create_user_exercise(db_session, setup_data):
    user_id, ex_id = setup_data
    repo = UserExerciseRepository(db_session)
    in_data = UserExerciseCreateInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today()
    )
    
    item = await repo.create(in_data)
    
    assert item.user_id == user_id
    assert item.exercise_id == ex_id
    assert item.sets == 3

@pytest.mark.asyncio
async def test_get_user_exercise(db_session, setup_data):
    user_id, ex_id = setup_data
    repo = UserExerciseRepository(db_session)
    in_data = UserExerciseCreateInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today()
    )
    created = await repo.create(in_data)
    
    fetched = await repo.get_by_id(str(created.id))
    
    assert fetched is not None
    assert fetched.id == created.id

@pytest.mark.asyncio
async def test_update_user_exercise(db_session, setup_data):
    user_id, ex_id = setup_data
    repo = UserExerciseRepository(db_session)
    in_data = UserExerciseCreateInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today()
    )
    created = await repo.create(in_data)
    
    update_in = UserExerciseUpdateInput(sets=4)
    updated = await repo.update(str(created.id), update_in)
    
    assert updated is not None
    assert updated.sets == 4

@pytest.mark.asyncio
async def test_delete_user_exercise(db_session, setup_data):
    user_id, ex_id = setup_data
    repo = UserExerciseRepository(db_session)
    in_data = UserExerciseCreateInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today()
    )
    created = await repo.create(in_data)
    
    success = await repo.delete(str(created.id))
    
    assert success is True
    fetched = await repo.get_by_id(str(created.id))
    assert fetched is None
