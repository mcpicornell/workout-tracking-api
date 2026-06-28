from typing import Protocol

from .jobs_use_cases_types import JobStatus, JobStoragePort, UpdateJobInput
from .workout_messages_use_cases_types import (
    ProcessWorkoutMessageInput,
    ProcessWorkoutMessagePortInput,
    WorkoutMessageProcessorPort,
)


class WorkoutMessagesUseCases(Protocol):
    async def process_workout_message(
        self, input: ProcessWorkoutMessageInput
    ) -> None: ...


class DefaultWorkoutMessagesUseCases(WorkoutMessagesUseCases):
    def __init__(
        self,
        message_processor_port: WorkoutMessageProcessorPort,
        job_storage_port: JobStoragePort,
    ):
        self._message_processor_port = message_processor_port
        self._job_storage_port = job_storage_port

    async def process_workout_message(
        self,
        input: ProcessWorkoutMessageInput,
    ) -> None:
        try:
            port_output = await self._message_processor_port.process_workout_message(
                ProcessWorkoutMessagePortInput(message=input.message)
            )

            await self._job_storage_port.update_job(
                UpdateJobInput(
                    id=input.job_id,
                    status=JobStatus.COMPLETED,
                    result=port_output.result,
                )
            )
        except Exception as e:
            await self._job_storage_port.update_job(
                UpdateJobInput(id=input.job_id, status=JobStatus.FAILED, result=str(e))
            )
            raise
