from workout_tracking.domain.workout_messages_use_cases_types import (
    ProcessWorkoutMessagePortInput,
    ProcessWorkoutMessagePortOutput,
    WorkoutMessageProcessorPort,
)
from workout_tracking.infra.agents.workout_agent import WorkoutAgent

from .workout_message_processor_adapter_types import (
    map_process_workout_message_domain_to_infra,
    map_process_workout_message_infra_to_domain,
)


class WorkoutMessageProcessorAdapter(WorkoutMessageProcessorPort):
    def __init__(self, workout_agent: WorkoutAgent):
        self._workout_agent = workout_agent

    async def process_workout_message(
        self, input: ProcessWorkoutMessagePortInput
    ) -> ProcessWorkoutMessagePortOutput:
        infra_input = map_process_workout_message_domain_to_infra(input)
        infra_output = await self._workout_agent.process_workout_message(infra_input)
        return map_process_workout_message_infra_to_domain(infra_output)
