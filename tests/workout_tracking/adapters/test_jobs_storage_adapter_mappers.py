from datetime import datetime, timezone
from uuid import uuid4

from workout_tracking.adapters.jobs_storage_adapter_mappers import (
    map_domain_job_to_infra_create_input,
    map_domain_job_to_infra_delete_input,
    map_domain_job_to_infra_get_by_id_input,
    map_domain_job_to_infra_update_input,
    map_infra_job_output_to_domain,
)
from workout_tracking.domain.jobs_use_cases_types import (
    CreateJobPortInput,
    DeleteJobPortInput,
    GetJobByIdPortInput,
    JobStatus,
    UpdateJobPortInput,
)
from workout_tracking.infra.repositories.job_repository_types import (
    CreateJobInput,
    DeleteJobInput,
    GetJobByIdInput,
    JobDB,
    UpdateJobInput,
)


def test_map_infra_job_output_to_domain():
    infra_output = JobDB(
        id=uuid4(),
        description="Test Description",
        status=JobStatus.COMPLETED,
        result="Test Result",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    domain_job = map_infra_job_output_to_domain(infra_output)

    assert domain_job.id == infra_output.id
    assert domain_job.description == infra_output.description
    assert domain_job.status == infra_output.status
    assert domain_job.result == infra_output.result
    assert domain_job.created_at == infra_output.created_at
    assert domain_job.updated_at == infra_output.updated_at


def test_map_infra_job_output_to_domain_with_none_result():
    infra_output = JobDB(
        id=uuid4(),
        description="Test Description",
        status=JobStatus.PENDING,
        result=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    domain_job = map_infra_job_output_to_domain(infra_output)
    
    assert domain_job.result is None


def test_map_domain_job_to_infra_create_input():
    domain_input = CreateJobPortInput(
        description="Test Description", status=JobStatus.PENDING
    )

    infra_input = map_domain_job_to_infra_create_input(domain_input)

    assert isinstance(infra_input, CreateJobInput)
    assert infra_input.description == domain_input.description
    assert infra_input.status == domain_input.status


def test_map_domain_job_to_infra_update_input():
    job_id = uuid4()
    domain_input = UpdateJobPortInput(
        id=job_id, status=JobStatus.COMPLETED, result="Test Result"
    )

    infra_input = map_domain_job_to_infra_update_input(domain_input)

    assert isinstance(infra_input, UpdateJobInput)
    assert infra_input.id == domain_input.id
    assert infra_input.status == domain_input.status
    assert infra_input.result == domain_input.result


def test_map_domain_job_to_infra_delete_input():
    job_id = uuid4()
    domain_input = DeleteJobPortInput(job_id=job_id)

    infra_input = map_domain_job_to_infra_delete_input(domain_input)

    assert isinstance(infra_input, DeleteJobInput)
    assert infra_input.id == domain_input.job_id


def test_map_domain_job_to_infra_get_by_id_input():
    job_id = uuid4()
    domain_input = GetJobByIdPortInput(job_id=job_id)

    infra_input = map_domain_job_to_infra_get_by_id_input(domain_input)

    assert isinstance(infra_input, GetJobByIdInput)
    assert infra_input.id == domain_input.job_id
