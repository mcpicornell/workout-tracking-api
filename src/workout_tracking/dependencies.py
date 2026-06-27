from sqlalchemy.ext.asyncio import AsyncSession
from .infra.db.database import AsyncSessionLocal
from .infra.repositories.user_repository import UserRepository
from .infra.repositories.exercise_repository import ExerciseRepository
from .infra.repositories.user_exercise_repository import UserExerciseRepository

class InfraDependencies:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.exercise_repository = ExerciseRepository(session)
        self.user_exercise_repository = UserExerciseRepository(session)

class AdaptersDependencies:
    def __init__(self, infra: InfraDependencies):
        self.infra = infra

class DomainDependencies:
    def __init__(self, adapters: AdaptersDependencies):
        self.adapters = adapters

class Dependencies:
    def __init__(self, session: AsyncSession):
        self.infra_dependencies = InfraDependencies(session)
        self.adapters_dependencies = AdaptersDependencies(self.infra_dependencies)
        self.domain_dependencies = DomainDependencies(self.adapters_dependencies)

async def get_dependencies() -> Dependencies:
    async with AsyncSessionLocal() as session:
        return Dependencies(session)
