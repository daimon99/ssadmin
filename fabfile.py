# coding:utf8

import os

from fabric.api import env, lcd, local

current_dir = os.getcwd()
env.project_name = 'turing'
env.branch = 'master'


def init():
    """初始化文件目录"""
    local('mkdir logs')


def export_req():
    """制作python依赖文件"""
    local('pip freeze > requirements.txt')


def deploy():
    """正常部署应用"""
    with lcd('playbook'):
        local('ansible-playbook playbook.yml')


def migrate():
    """生成并导入数据库脚本"""
    with lcd('src'):
        local('python manage.py makemigrations')
        local('python manage.py migrate')


def quick():
    """快速部署应用"""
    with lcd('playbook'):
        local('ansible-playbook playbook.yml --tags=quick')


def sync(msg=''):
    """仅同步代码"""
    if msg:
        # msg有值，则提交代码
        local('git add .')
        local('git commit -am "%s"' % msg)
        local('git push')
    with lcd('playbook'):
        local('ansible-playbook playbook.yml --tags=sync')


def install_roles():
    """安装ansible roles"""
    with lcd('playbook'):
        local('ansible-galaxy install -r requirements.yml -p ./roles -f -c')


def run():
    """运行应用"""
    local('python src/manage.py runserver 8000')


def push(msg):
    """推送代码"""
    with lcd(current_dir):
        local('git add .')
        local('git status')
        p = raw_input('继续吗？回车表示继续，其它表示退出')
        if p:
            print p
            return
        local('git commit -am "{}"'.format(msg))
        local('git push')
