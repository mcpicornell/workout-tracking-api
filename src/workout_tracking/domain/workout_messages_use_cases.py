from datetime import date
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
        workout_message_processor_port: WorkoutMessageProcessorPort,
        job_storage_port: JobStoragePort,
    ):
        self._workout_message_processor_port = workout_message_processor_port
        self._job_storage_port = job_storage_port

    async def process_workout_message(
        self,
        input: ProcessWorkoutMessageInput,
    ) -> None:
        try:
            process_workout_message_output = (
                await self._workout_message_processor_port.process_workout_message(
                    ProcessWorkoutMessagePortInput(
                        message=input.message,
                        user_id=input.user_id,
                        job_id=input.job_id,
                        workout_date=date.today(),
                    )
                )
            )

            await self._job_storage_port.update_job(
                UpdateJobInput(
                    id=input.job_id,
                    status=JobStatus.COMPLETED,
                    result=process_workout_message_output.result,
                )
            )
        except Exception as e:
            await self._job_storage_port.update_job(
                UpdateJobInput(id=input.job_id, status=JobStatus.FAILED, result=str(e))
            )
            raise
