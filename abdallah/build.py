from abdallah.docker_utils import get_docker_client, get_job_host_config


def run_build(project, commit='master'):
    build = project.build_set.create(
        commit=commit,
        project=project,
        configuration=project.configuration)
    jobs_configuration = build.get_jobs_configuration()
    for job_attr in jobs_configuration[:1]:
        job = build.job_set.create(build=build)
        run_job(job, job_attr, commit=commit)
    return build


def run_job(job, job_attr, commit='master'):
    docker_client = get_docker_client()
    volumes, host_config = get_job_host_config(job, job_attr)
    container_attrs = docker_client.create_container(
        image='python:2',
        command='bash /job.sh',
        name=job.container_name,
        environment=job_attr['env'],
        volumes=volumes)
    docker_client.start(resource_id=container_attrs,
                        binds=host_config)
