import pytest
from uuid import uuid4
from workout_tracking.infra.repositories.exercise_repository import ExerciseRepository, DefaultExerciseRepository
from workout_tracking.infra.repositories.exercise_repository_types import (
    CreateExerciseInput,
    UpdateExerciseInput,
    GetExerciseByIdInput,
    GetExerciseByJobIdInput,
    DeleteExerciseInput
)
from workout_tracking.infra.db.models import JobModel, JobStatus

@pytest.fixture
async def job_id(db_session):
    job = JobModel(description="Test Job Description", status=JobStatus.PENDING)
    db_session.add(job)
    await db_session.commit()
    return job.id

@pytest.mark.asyncio
async def test_create_exercise(db_session, job_id):
    repo = DefaultExerciseRepository(db_session)
    ex_in = CreateExerciseInput(name="Push-up", description="Basic bodyweight exercise", job_id=job_id)
    
    exercise = await repo.create_exercise(ex_in)
    
    assert exercise.name == "Push-up"
    assert exercise.id is not None
    assert exercise.job_id == job_id

@pytest.mark.asyncio
async def test_get_exercise(db_session, job_id):
    repo = DefaultExerciseRepository(db_session)
    ex_in = CreateExerciseInput(name="Squat", job_id=job_id)
    created = await repo.create_exercise(ex_in)
    
    fetched = await repo.get_exercise_by_id(GetExerciseByIdInput(id=str(created.id)))
    
    assert fetched is not None
    assert fetched.name == "Squat"

@pytest.mark.asyncio
async def test_update_exercise(db_session, job_id):
    repo = DefaultExerciseRepository(db_session)
    ex_in = CreateExerciseInput(name="Squat", job_id=job_id)
    created = await repo.create_exercise(ex_in)
    
    update_in = UpdateExerciseInput(id=str(created.id), description="Leg day focus")
    updated = await repo.update_exercise(update_in)
    
    assert updated is not None
    assert updated.description == "Leg day focus"

@pytest.mark.asyncio
async def test_delete_exercise(db_session, job_id):
    repo = DefaultExerciseRepository(db_session)
    ex_in = CreateExerciseInput(name="Squat", job_id=job_id)
    created = await repo.create_exercise(ex_in)
    
    success = await repo.delete_exercise(DeleteExerciseInput(id=str(created.id)))
    
    assert success is True
    fetched = await repo.get_exercise_by_id(GetExerciseByIdInput(id=str(created.id)))
    assert fetched is None

@pytest.mark.asyncio
async def test_get_exercises_by_job_id(db_session, job_id):
    repo = DefaultExerciseRepository(db_session)
    ex_in = CreateExerciseInput(name="Squat", job_id=job_id)
    await repo.create_exercise(ex_in)
    
    ex_in2 = CreateExerciseInput(name="Push-up", job_id=job_id)
    await repo.create_exercise(ex_in2)
    
    exercises = await repo.get_exercises_by_job_id(GetExerciseByJobIdInput(job_id=job_id))
    
    assert len(exercises) == 2
