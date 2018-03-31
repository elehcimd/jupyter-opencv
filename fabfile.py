from fabric.api import local
from fabric.decorators import task
from os.path import dirname, realpath

project_name = 'jupyter-opencv'


@task
def docker_exec(cmdline):
    """
    Execute command in running docker container
    :param cmdline: command to be executed
    """
    local('docker exec -ti {} {}'.format(project_name, cmdline))


@task
def docker_build(options=''):
    """
    Build docker image
    """

    docker_stop()
    local('docker build {} -t {} .'.format(options, project_name))


@task
def docker_start(map_repos='true'):
    """
    Start docker container
    """

    docker_stop()
    map_repos = '-v {}:/playground'.format(dirname(realpath(__file__))) if map_repos == 'true' else ''
    local('docker run --rm --name {project_name} -d -ti -p 127.0.0.1:8889:8888 {map_repos} -t {project_name}'.format(
        project_name=project_name,
        map_repos=map_repos))


@task
def docker_stop():
    """
    Stop docker container
    """
    local('docker kill {} || true'.format(project_name))


@task
def docker_sh():
    """
    Execute command in docker container
    """
    docker_exec('/bin/bash')


@task
def docker_logs():
    """
    Print stdout/stderr from container entrypoint
    :return:
    """
    local('docker logs {} -f'.format(project_name))


@task
def test(params=''):
    """
    Run all tests in docker container
    :param params: parameters to py.test
    """
    docker_exec('py.test {}'.format(params))


@task
def test_sx(params=''):
    """
    Execute all tests in docker container printing output and terminating tests at first failure
    :param params: parameters to py.test
    """
    docker_exec('py.test -sx {}'.format(params))


@task
def test_pep8():
    """
    Execute  only pep8 test in docker container
    """
    docker_exec('py.test tests/test_pep8.py')


@task
def fix_pep8():
    """
    Fix a few common and easy PEP8 mistakes in docker container
    """
    docker_exec('autopep8 --select E251,E303,W293,W291,W391,W292,W391,E302 --aggressive --in-place --recursive .')
