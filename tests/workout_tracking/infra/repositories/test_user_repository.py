import pytest
from uuid import uuid4
from workout_tracking.infra.repositories.user_repository import UserRepository, DefaultUserRepository
from workout_tracking.infra.repositories.user_repository_types import (
    CreateUserInput, 
    UpdateUserInput,
    GetUserByIdInput,
    GetUserByEmailInput,
    GetUserByJobIdInput,
    DeleteUserInput
)
from workout_tracking.infra.db.models import JobModel, JobStatus, UserModel
from datetime import datetime

@pytest.fixture
async def job_id(db_session):
    job = JobModel(id=uuid4(), name="Test Job", description="Test Job Description", status=JobStatus.PENDING, job_id=uuid4())
    db_session.add(job)
    await db_session.commit()
    return job.id

@pytest.fixture
async def setup_data(db_session, job_id):
    user = UserModel(id=uuid4(), email="user@test.com", hashed_password="pw", job_id=job_id)
    db_session.add(user)
    await db_session.commit()
    return user.id, job_id

@pytest.mark.asyncio
async def test_create_user(db_session, job_id):
    repo = DefaultUserRepository(db_session)
    user_in = CreateUserInput(email="test@example.com", password="password123", job_id=job_id)
    user = await repo.create_user(user_in)
    
    assert user.email == "test@example.com"
    assert user.id is not None
    assert user.job_id == job_id

@pytest.mark.asyncio
async def test_get_user_by_id(db_session, setup_data):
    user_id, _ = setup_data
    repo = DefaultUserRepository(db_session)
    
    fetched = await repo.get_user_by_id(GetUserByIdInput(id=str(user_id)))
    assert fetched is not None
    assert fetched.id == user_id

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(db_session):
    repo = DefaultUserRepository(db_session)
    user = await repo.get_user_by_id(GetUserByIdInput(id="nonexistent"))
    assert user is None

@pytest.mark.asyncio
async def test_get_user_by_email(db_session, setup_data):
    user_id, _ = setup_data
    repo = DefaultUserRepository(db_session)
    user = await repo.get_user_by_id(GetUserByIdInput(id=str(user_id)))
    email = user.email
    
    fetched = await repo.get_user_by_email(GetUserByEmailInput(email=email))
    assert fetched is not None
    assert fetched.email == email

@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session):
    repo = DefaultUserRepository(db_session)
    user = await repo.get_user_by_email(GetUserByEmailInput(email="nonexistent@example.com"))
    assert user is None

@pytest.mark.asyncio
async def test_update_user(db_session, setup_data):
    user_id, _ = setup_data
    repo = DefaultUserRepository(db_session)
    
    update_in = UpdateUserInput(id=str(user_id), email="updated@example.com", is_active=False)
    updated = await repo.update_user(update_in)
    
    assert updated is not None
    assert updated.email == "updated@example.com"
    assert updated.is_active is False

@pytest.mark.asyncio
async def test_update_user_not_found(db_session):
    repo = DefaultUserRepository(db_session)
    update_in = UpdateUserInput(id="nonexistent", email="updated@example.com")
    updated = await repo.update_user(update_in)
    assert updated is None

@pytest.mark.asyncio
async def test_delete_user(db_session, setup_data):
    user_id, _ = setup_data
    repo = DefaultUserRepository(db_session)
    
    success = await repo.delete_user(DeleteUserInput(id=str(user_id)))
    assert success is True
    
    fetched = await repo.get_user_by_id(GetUserByIdInput(id=str(user_id)))
    assert fetched is None

@pytest.mark.asyncio
async def test_delete_user_not_found(db_session):
    repo = DefaultUserRepository(db_session)
    success = await repo.delete_user(DeleteUserInput(id="nonexistent"))
    assert success is False

@pytest.mark.asyncio
async def test_get_users_by_job_id(db_session, job_id):
    repo = DefaultUserRepository(db_session)
    user = UserModel(email="job_user@test.com", hashed_password="pw", job_id=job_id)
    db_session.add(user)
    await db_session.commit()
    
    users = await repo.get_users_by_job_id(GetUserByJobIdInput(job_id=job_id))
    assert len(users) == 1
    assert users[0].email == "job_user@test.com"
