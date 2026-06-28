import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from workout_tracking.dependencies import DependenciesBuilder, Dependencies

@pytest.fixture
def mock_session():
    return MagicMock(spec=AsyncSession)

@pytest.fixture
def builder():
    return DependenciesBuilder()

def test_build_dependencies(builder, mock_session):
    # This will likely fail due to the bugs I found, but it's the first step
    deps = builder.build(mock_session)
    assert isinstance(deps, Dependencies)
    assert deps.infra_dependencies is not None
    assert deps.adapters_dependencies is not None
    assert deps.domain_dependencies is not None
