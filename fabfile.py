# coding:utf8

import os

from fabric.api import env, lcd, local

current_dir = os.getcwd()
env.project_name = 'turing'
env.branch = 'master'


def export_req():
    """制作python依赖文件"""
    local('pip freeze > requirements.txt')


def deploy():
    """正常部署应用"""
    with lcd('playbook'):
        local('ansible-playbook playbook.yml')


def quick():
    """快速部署应用"""
    with lcd('playbook'):
        local('ansible-playbook playbook.yml --tags=quick')


def install_roles():
    """安装ansible roles"""
    with lcd('playbook'):
        local('ansible-galaxy install -r requirements.yml -p ./roles -f -c')


def migrate():
    """同步模型"""
    with lcd('src'):
        local('python manage.py makemigrations')
        local('python manage.py migrate')


def run():
    """运行应用"""
    local('python src/manage.py runserver 8000')
