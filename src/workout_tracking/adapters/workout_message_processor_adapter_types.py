from workout_tracking.domain.workout_messages_use_cases_types import (
    ProcessWorkoutMessagePortInput,
    ProcessWorkoutMessagePortOutput,
)
from workout_tracking.infra.agents.workout_agent_types import (
    ProcessWorkoutMessageInput as InfraProcessWorkoutMessageInput,
)
from workout_tracking.infra.agents.workout_agent_types import (
    ProcessWorkoutMessageOutput as InfraProcessWorkoutMessageOutput,
)


def map_process_workout_message_domain_to_infra(
    input: ProcessWorkoutMessagePortInput,
) -> InfraProcessWorkoutMessageInput:
    return InfraProcessWorkoutMessageInput(
        user_id=input.user_id,
        job_id=input.job_id,
        message=input.message,
        workout_date=input.workout_date,
    )


def map_process_workout_message_infra_to_domain(
    output: InfraProcessWorkoutMessageOutput,
) -> ProcessWorkoutMessagePortOutput:
    return ProcessWorkoutMessagePortOutput(
        result=output.content,
    )
