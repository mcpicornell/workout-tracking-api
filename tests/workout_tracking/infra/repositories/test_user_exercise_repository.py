import pytest
from datetime import date
from workout_tracking.infra.repositories.user_exercise_repository import UserExerciseRepository, DefaultUserExerciseRepository
from workout_tracking.infra.repositories.user_exercise_repository_types import (
    CreateUserExerciseInput, 
    UpdateUserExerciseInput,
    GetUserExerciseByIdInput,
    GetUserExerciseByJobIdInput,
    DeleteUserExerciseInput
)
from workout_tracking.infra.db.models import UserModel, ExerciseModel, JobModel, JobStatus
from uuid import uuid4

@pytest.fixture
async def job_id(db_session):
    job = JobModel(name="Test Job", description="Test Job Description", status=JobStatus.PENDING, job_id=uuid4())
    db_session.add(job)
    await db_session.commit()
    return job.id

@pytest.fixture
async def setup_data(db_session, job_id):
    user = UserModel(id=uuid4(), email="user@test.com", hashed_password="pw", job_id=job_id)
    ex = ExerciseModel(id=uuid4(), name="Squat", job_id=job_id)
    db_session.add(user)
    db_session.add(ex)
    await db_session.commit()
    return user.id, ex.id, job_id

@pytest.mark.asyncio
async def test_create_user_exercise(db_session, setup_data, job_id):
    user_id, ex_id, _ = setup_data
    repo = DefaultUserExerciseRepository(db_session)
    in_data = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    
    item = await repo.create_user_exercise(in_data)
    
    assert item.user_id == user_id
    assert item.exercise_id == ex_id
    assert item.sets == 3
    assert item.job_id == job_id

@pytest.mark.asyncio
async def test_get_user_exercise(db_session, setup_data):
    user_id, ex_id, job_id = setup_data
    repo = DefaultUserExerciseRepository(db_session)
    in_data = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    created = await repo.create_user_exercise(in_data)
    
    fetched = await repo.get_user_exercise_by_id(GetUserExerciseByIdInput(id=str(created.id)))
    
    assert fetched is not None
    assert fetched.id == created.id

@pytest.mark.asyncio
async def test_update_user_exercise(db_session, setup_data, job_id):
    user_id, ex_id, _ = setup_data
    repo = DefaultUserExerciseRepository(db_session)
    in_data = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    created = await repo.create_user_exercise(in_data)
    
    update_in = UpdateUserExerciseInput(id=str(created.id), sets=4)
    updated = await repo.update_user_exercise(update_in)
    
    assert updated is not None
    assert updated.sets == 4

@pytest.mark.asyncio
async def test_delete_user_exercise(db_session, setup_data):
    user_id, ex_id, job_id = setup_data
    repo = DefaultUserExerciseRepository(db_session)
    in_data = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    created = await repo.create_user_exercise(in_data)
    
    success = await repo.delete_user_exercise(DeleteUserExerciseInput(id=str(created.id)))
    
    assert success is True
    fetched = await repo.get_user_exercise_by_id(GetUserExerciseByIdInput(id=str(created.id)))
    assert fetched is None

@pytest.mark.asyncio
async def test_get_user_exercises_by_job_id(db_session, setup_data, job_id):
    user_id, ex_id, _ = setup_data
    repo = DefaultUserExerciseRepository(db_session)
    in_data = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    await repo.create_user_exercise(in_data)
    
    in_data2 = CreateUserExerciseInput(
        user_id=user_id, exercise_id=ex_id, sets=3, reps=10, weight=100, date=date.today(), job_id=job_id
    )
    await repo.create_user_exercise(in_data2)
    
    exercises = await repo.get_user_exercises_by_job_id(GetUserExerciseByJobIdInput(job_id=job_id))
    
    assert len(exercises) == 2
