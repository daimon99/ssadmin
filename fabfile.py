# coding:utf8

import os
import random
import string

import requests
from fabric.api import env, lcd, local, require
from fabric.colors import cyan
from fabric.operations import prompt

current_dir = os.getcwd()
env.project_name = 'turing'
env.branch = 'master'

def export_req():
    local('pip freeze > requirements.txt')

def deploy():
    with lcd('playbook'):
        local('ansible-playbook playbook.yml')
