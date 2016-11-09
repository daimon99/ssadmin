# coding:utf-8
import logging
import subprocess

log = logging.getLogger(__name__)


def add_user(port, password, limit):
    """创建ss用户
    >>> add_user(10001, 'daijian', '1g')
    用户已存在
    """
    port, password, limit = str(port), str(password), str(limit)
    log.debug(u'创建ss用户， port=%s, password=%s', port, password)
    ret = subprocess.check_output(['/data/prd/ss-bash/ssadmin.sh', 'add', port, password, limit])
    print ret

if __name__ == '__main__':
    import doctest
    doctest.testmod()