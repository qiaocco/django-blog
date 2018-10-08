"""
针对fabric 2.x
https://github.com/fabric/fabric/
"""
import os

from invoke import task
from jinja2 import Environment, FileSystemLoader, select_autoescape

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # local path
WORKSPACE_PATH = '/home/jason/workspace'
DEPLOY_PATH = os.path.join(WORKSPACE_PATH, 'django-blog')  # remote path
PYTHON_PATH = '/home/ubuntu/.venv/blog_env/bin/python'  # remote venv python path
PROCESS_COUNT = 1


@task
def deploy(c):
    """部署项目:
    1. 更新代码
        从git拉取最新代码
        上传环境变量配置文件.env
        收集静态文件
    2. 重启项目

    Usage:
        fab -H myserver -S ssh_config deploy 1.4 product
    """
    update_code(c, DEPLOY_PATH)
    restart_project(c)


def update_code(c, deploy_path):
    with c.cd(deploy_path):
        c.run('git pull')
    _upload_env(c, deploy_path)
    _collect_static(c, deploy_path)


def _upload_env(c, deploy_path):
    env_path = os.path.join(PROJECT_ROOT, '.envs', '.env.product')
    # TODO 远程创建.envs目录
    destination = os.path.join(deploy_path, '.envs', '.env.product')
    c.put(env_path, destination)


def _collect_static(c, deploy_path):
    manage_path = os.path.join(deploy_path, 'manage.py')
    venv_name = 'blog_py3.6_env'
    with c.prefix('source ~/.zshrc && workon {}'.format(venv_name)):
        c.run('{env} python {manage_path} collectstatic --noinput'.format(
            env='env DJANGO_BLOG_PROFILE=product',
            manage_path=manage_path
        ))


def restart_project(c):
    c.run(f'supervisorctl restart blog')
