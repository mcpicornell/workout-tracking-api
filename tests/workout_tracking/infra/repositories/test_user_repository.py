import pytest
from workout_tracking.infra.repositories.user_repository import UserRepository
from workout_tracking.infra.repositories.user_repository_types import UserCreateInput, UserUpdateInput

@pytest.mark.asyncio
async def test_create_user(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreateInput(email="test@example.com", password="password123")
    user = await repo.create(user_in)
    
    assert user.email == "test@example.com"
    assert user.id is not None

@pytest.mark.asyncio
async def test_get_user_by_id(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreateInput(email="test_id@example.com", password="password123")
    created = await repo.create(user_in)
    
    fetched = await repo.get_by_id(str(created.id))
    assert fetched is not None
    assert fetched.email == "test_id@example.com"

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_by_id("nonexistent")
    assert user is None

@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    repo = UserRepository(db_session)
    email = "test_email@example.com"
    user_in = UserCreateInput(email=email, password="password123")
    await repo.create(user_in)
    
    user = await repo.get_by_email(email)
    assert user is not None
    assert user.email == email

@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_by_email("nonexistent@example.com")
    assert user is None

@pytest.mark.asyncio
async def test_update_user(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreateInput(email="update@example.com", password="password123")
    created = await repo.create(user_in)
    
    update_in = UserUpdateInput(email="updated@example.com", is_active=False)
    updated = await repo.update(str(created.id), update_in)
    
    assert updated is not None
    assert updated.email == "updated@example.com"
    assert updated.is_active is False

@pytest.mark.asyncio
async def test_update_user_not_found(db_session):
    repo = UserRepository(db_session)
    update_in = UserUpdateInput(email="updated@example.com")
    updated = await repo.update("nonexistent", update_in)
    assert updated is None

@pytest.mark.asyncio
async def test_delete_user(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreateInput(email="delete@example.com", password="password123")
    created = await repo.create(user_in)
    
    success = await repo.delete(str(created.id))
    assert success is True
    
    fetched = await repo.get_by_id(str(created.id))
    assert fetched is None

@pytest.mark.asyncio
async def test_delete_user_not_found(db_session):
    repo = UserRepository(db_session)
    success = await repo.delete("nonexistent")
    assert success is False
