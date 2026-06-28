from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from workout_tracking.infra.agents.workout_agent import DefaultWorkoutAgent, WorkoutAgent
from workout_tracking.infra.agents.workout_agent_types import LLMSettings
from workout_tracking.adapters.jobs_storage_adapter import (
    JobsStorageAdapter,
)
from workout_tracking.adapters.workout_message_processor_adapter import (
    WorkoutMessageProcessorAdapter,
)
from workout_tracking.domain.jobs_use_cases import DefaultJobsUseCases, JobsUseCases
from workout_tracking.domain.workout_messages_use_cases import (
    DefaultWorkoutMessagesUseCases,
    WorkoutMessagesUseCases,
)

from .infra.db.database import AsyncSessionLocal
from .infra.repositories.exercise_repository import (
    DefaultExerciseRepository,
    ExerciseRepository,
)
from .infra.repositories.job_repository import DefaultJobRepository, JobRepository
from .infra.repositories.user_exercise_repository import (
    DefaultUserExerciseRepository,
    UserExerciseRepository,
)
from .infra.repositories.user_repository import DefaultUserRepository, UserRepository


@dataclass(frozen=True, slots=True)
class InfraDependencies:
    user_repository: UserRepository
    exercise_repository: ExerciseRepository
    user_exercise_repository: UserExerciseRepository
    job_repository: JobRepository
    workout_agent: WorkoutAgent


@dataclass(frozen=True, slots=True)
class AdaptersDependencies:
    jobs_storage_adapter: JobsStorageAdapter
    workout_message_processor_adapter: WorkoutMessageProcessorAdapter


@dataclass(frozen=True, slots=True)
class DomainDependencies:
    jobs_use_cases: JobsUseCases
    workout_messages_use_cases: WorkoutMessagesUseCases


@dataclass(frozen=True, slots=True)
class Dependencies:
    infra_dependencies: InfraDependencies
    adapters_dependencies: AdaptersDependencies
    domain_dependencies: DomainDependencies


class DependenciesBuilder:
    def build(self, session: AsyncSession) -> Dependencies:
        infra_dependencies = self._build_infra_dependencies(session)
        adapters_dependencies = self._build_adapters_dependencies(infra_dependencies)
        domain_dependencies = self._build_domain_dependencies(adapters_dependencies)
        return Dependencies(
            infra_dependencies=infra_dependencies,
            adapters_dependencies=adapters_dependencies,
            domain_dependencies=domain_dependencies,
        )

    def _build_infra_dependencies(self, session: AsyncSession) -> InfraDependencies:
        # Note: LLMSettings should ideally come from a config file
        settings = LLMSettings(name="gemini-pro", api_key="fake_key")
        workout_agent = DefaultWorkoutAgent(
            exercise_repository=DefaultExerciseRepository(session),
            user_exercise_repository=DefaultUserExerciseRepository(session),
            checkpointer=MemorySaver(),
            settings=settings,
        )
        return InfraDependencies(
            user_repository=DefaultUserRepository(session),
            exercise_repository=DefaultExerciseRepository(session),
            user_exercise_repository=DefaultUserExerciseRepository(session),
            job_repository=DefaultJobRepository(session),
            workout_agent=workout_agent,
        )

    def _build_adapters_dependencies(
        self, infra: InfraDependencies
    ) -> AdaptersDependencies:
        return AdaptersDependencies(
            jobs_storage_adapter=JobsStorageAdapter(infra.job_repository),
            workout_message_processor_adapter=WorkoutMessageProcessorAdapter(
                infra.workout_agent
            ),
        )

    def _build_domain_dependencies(
        self,
        adapters: AdaptersDependencies,
    ) -> DomainDependencies:
        return DomainDependencies(
            jobs_use_cases=DefaultJobsUseCases(
                job_storage_port=adapters.jobs_storage_adapter
            ),
            workout_messages_use_cases=DefaultWorkoutMessagesUseCases(
                workout_message_processor_port=adapters.workout_message_processor_adapter,
                job_storage_port=adapters.jobs_storage_adapter,
            ),
        )


async def get_dependencies() -> Dependencies:
    async with AsyncSessionLocal() as session:
        return DependenciesBuilder().build(session)
