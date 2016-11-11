# coding:utf-8
import functools
import logging
import re
import subprocess

from .exceptions import SSError

log = logging.getLogger(__name__)

SS_ADMIN = '/data/prd/ss-bash/ssadmin.sh'
re_show = re.compile('^(?P<port>\d*)\s*(?P<limit>\d*)\(\S*\)\s*(?P<used>\d*)\(\S*\)\s*(?P<remaining>\d*)\(\S*\)')


def log_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.info('%s(%s, %s)', func.__name__, args, kwargs)
            ret = func(*args, **kwargs)
            log.info(ret)
            return ret
        except subprocess.CalledProcessError as e:
            log.error('调用出错：%s, %s, %s', e.cmd, e.returncode, e.output)
            raise e
        except Exception as e:
            log.error(e)
            raise e

    return wrapper


@log_wrapper
def add(port, password, limit):
    """创建ss用户

    >>> add(10001, 'daijian', '1g')
    ['/data/prd/ss-bash/ssadmin.sh', 'add', '10001', 'daijian', '1g'] 1 用户已存在!
    """
    port, password, limit = str(port), str(password), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'add', port, password, limit], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def clim(port, limit):
    """修改用户流量"""
    port, limit = str(port), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'clim', port, limit], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def rlim(port):
    """用户流量限制置0"""
    port = str(port)
    ret = subprocess.check_output([SS_ADMIN, 'rlim', port], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def rused(port):
    """用户使用量置0"""
    port = str(port)
    ret = subprocess.check_output([SS_ADMIN, 'rused', port], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def change(port, password, limit):
    """修改用户"""
    port, password, limit = str(port), str(password), str(limit)
    ret = subprocess.check_output([SS_ADMIN, 'change', port, password, limit], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def soft_restart():
    """在不影响现有连接的情况下重启ss服务。用于ss服务参数修改，和手动直接修改配置文件后，重启ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'soft_restart'], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def restart():
    """重启ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'restart'], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def start():
    """启动ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'start'], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def stop():
    """停止ss服务。"""
    ret = subprocess.check_output([SS_ADMIN, 'stop'], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def show():
    """显示所有用户流量信息"""
    ret = subprocess.check_output([SS_ADMIN, 'show'], stderr=subprocess.STDOUT)
    return ret


@log_wrapper
def show_port(port):
    """显示指定用户流量信息"""
    ret = subprocess.check_output([SS_ADMIN, 'show', str(port)], stderr=subprocess.STDOUT)
    lines = ret.splitlines()
    if len(lines) == 2:
        detail = lines[1]
        result_parsed = re_show.match(detail).groupdict()
        return result_parsed
    else:
        log.error('返回结果格式不对，请注意检查: %s', ret)
        raise SSError('返回结果格式不对，请注意检查：%s' % ret)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
