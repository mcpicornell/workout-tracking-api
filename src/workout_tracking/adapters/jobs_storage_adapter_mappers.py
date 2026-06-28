from workout_tracking.domain.jobs_use_cases_types import (
    CreateJobPortInput,
    DeleteJobPortInput,
    GetJobByIdPortInput,
    Job,
    UpdateJobPortInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobInput as InfraCreateJobInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobOutput as InfraCreateJobOutput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    DeleteJobInput as InfraDeleteJobInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    GetJobByIdInput as InfraGetJobByIdInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    GetJobByIdOutput as InfraGetJobByIdOutput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    UpdateJobInput as InfraUpdateJobInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    UpdateJobOutput as InfraUpdateJobOutput,
)

type InfraOutput = InfraCreateJobOutput | InfraUpdateJobOutput | InfraGetJobByIdOutput


def map_infra_job_output_to_domain(infra_output: InfraOutput) -> Job:
    return Job(
        id=infra_output.id,
        description=infra_output.description,
        status=infra_output.status,
        result=infra_output.result,
        created_at=infra_output.created_at,
        updated_at=infra_output.updated_at,
    )


def map_domain_job_to_infra_create_input(
    domain_input: CreateJobPortInput,
) -> InfraCreateJobInput:
    return InfraCreateJobInput(
        description=domain_input.description,
        status=domain_input.status,
    )


def map_domain_job_to_infra_update_input(
    domain_input: UpdateJobPortInput,
) -> InfraUpdateJobInput:
    return InfraUpdateJobInput(
        id=domain_input.id,
        status=domain_input.status,
        result=domain_input.result,
    )


def map_domain_job_to_infra_delete_input(
    domain_input: DeleteJobPortInput,
) -> InfraDeleteJobInput:
    return InfraDeleteJobInput(
        id=domain_input.job_id,
    )


def map_domain_job_to_infra_get_by_id_input(
    domain_input: GetJobByIdPortInput,
) -> InfraGetJobByIdInput:
    return InfraGetJobByIdInput(
        id=domain_input.job_id,
    )
