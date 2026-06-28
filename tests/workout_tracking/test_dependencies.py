import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from workout_tracking.dependencies import DependenciesBuilder, Dependencies
from workout_tracking.settings import Settings

@pytest.fixture
def mock_session():
    return MagicMock(spec=AsyncSession)

@pytest.fixture
def mock_settings():
    return MagicMock(spec=Settings)

@pytest.fixture
def builder():
    return DependenciesBuilder()

def test_build_dependencies(builder, mock_session, mock_settings):
    mock_settings.DEFAULT_LLM_MODEL = "gemini-pro"
    mock_settings.GEMINI_API_KEY = "fake-key"
    mock_settings.SECRET_AUTH_KEY = "fake-secret"
    
    # This will likely fail due to the bugs I found, but it's the first step
    deps = builder.build(mock_session, mock_settings)
    assert isinstance(deps, Dependencies)
    assert deps.infra_dependencies is not None
    assert deps.adapters_dependencies is not None
    assert deps.domain_dependencies is not None
