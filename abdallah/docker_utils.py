import tempfile
import docker
from django.template import loader, Context


def get_docker_client():
    """
    Get configured docker client.

    :param params: Settings module with Docker client configuration
    :type params: :mod:`abdallah.settings`

    :returns: Configured Docker client
    :rtype: :class:`docker.Client`
    """
    from abdallah import settings
    client = docker.Client(base_url=settings.DOCKER['BASE_URL'],
                           version=settings.DOCKER['VERSION'],
                           timeout=settings.DOCKER['TIMEOUT'],
                           tls=settings.DOCKER['TLS'])
    return client


def get_job_host_config(job, job_attr):
    template = loader.get_template('abdallah/job.sh')
    context_dict = job_attr.copy()
    context_dict.update({'job': job})
    context = Context(context_dict)
    init_script_path = tempfile.mktemp('abdallah')
    volumes = [init_script_path]
    with open(init_script_path, 'w') as init_script:
        init_script.write(template.render(context))
    # host_config = docker.utils.create_host_config(binds=[
    #     '/init.sh:%s:ro' % init_script_path,
    # ])
    host_config = {
        init_script_path: {'bind': '/job.sh', 'ro': True}
    }
    return volumes, host_config
