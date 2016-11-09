# coding:utf-8
import logging
import subprocess

log = logging.getLogger(__name__)


def add_user(port, password):
    """创建ss用户"""
    log.debug(u'创建ss用户， port=%s, password=%s', port, password)
    ret = subprocess.check_output(['/data/prd/ss-bash/ssadmin.sh', 'show'])
    print type(ret), ret
