#!/usr/bin/env python
# A script to set the admin credentials
# Assumes two environment variables
#
# PROJECT_DIR: the project directory (e.g., ~/projname)
# ADMIN_PASSWORD: admin user's password

import os
import sys

import django

os.environ.setdefault('PROJECT_DIR', '../src')
os.environ.setdefault('ADMIN_PASSWORD', 'hello88765')

proj_dir = os.path.expanduser(os.environ['PROJECT_DIR'])
sys.path.append(proj_dir)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'ssadmin.settings'

# from ssadmin import settings as ssadmin_settings
# from django.conf import settings
# settings.configure(default_settings=ssadmin_settings)
django.setup()
from django.contrib.auth.models import User

u, _ = User.objects.get_or_create(username='hxt')
u.is_staff = u.is_superuser = True
u.set_password(os.environ['ADMIN_PASSWORD'])
u.save()
