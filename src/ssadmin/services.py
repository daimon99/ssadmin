# coding:utf-8
import functools
import logging
import subprocess

log = logging.getLogger(__name__)

SS_ADMIN = '/data/prd/ss-bash/ssadmin.sh'


def log_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.info('%s(%s, %s)', func.__name__, args, kwargs)
            ret = func(*args, **kwargs)
            log.info(ret)
            return ret
        except subprocess.CalledProcessError as e:
            log.error(e)
            return e.returncode
        except OSError as e:
            log.error(e)
            return e.errno

    return wrapper


@log_wrapper
def add(port, password, limit):
    """创建ss用户

    >>> add(10001, 'daijian', '1g')
    ['/data/prd/ss-bash/ssadmin.sh', 'add', '10001', 'daijian', '1g'] 1 用户已存在!
    """
    port, password, limit = str(port), str(password), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'add', port, password, limit])
    return ret


@log_wrapper
def clim(port, limit):
    """修改用户流量"""
    port, limit = str(port), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'clim', port, limit])
    return ret


@log_wrapper
def rlim(port):
    """用户流量限制置0"""
    port = str(port)
    ret = subprocess.check_output([SS_ADMIN, 'rlim', port])
    return ret


@log_wrapper
def rused(port):
    """用户使用量置0"""
    port = str(port)
    ret = subprocess.check_output([SS_ADMIN, 'rused', port])
    return ret


@log_wrapper
def change(port, password, limit):
    """修改用户"""
    port, password, limit = str(port), str(password), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'change', port, password, limit])
    return ret


@log_wrapper
def soft_restart():
    """在不影响现有连接的情况下重启ss服务。用于ss服务参数修改，和手动直接修改配置文件后，重启ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'soft_restart'])
    return ret


@log_wrapper
def restart():
    """重启ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'restart'])
    return ret


@log_wrapper
def start():
    """启动ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'start'])
    return ret


@log_wrapper
def stop():
    """停止ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'stop'])
    return ret


@log_wrapper
def show():
    """显示所有用户流量信息"""
    ret = subprocess.check_output([SS_ADMIN, 'show'])
    return ret


@log_wrapper
def show_port(port):
    """显示指定用户流量信息"""
    ret = subprocess.check_output([SS_ADMIN, 'show', str(port)], stderr=subprocess.STDOUT)
    return ret


if __name__ == '__main__':
    import doctest

    doctest.testmod()
