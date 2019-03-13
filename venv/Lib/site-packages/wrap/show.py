import logging

import functools

import time
from logcc.util.table import trace_table

from wrap.exception import safe


def show(name='default', text=None, level='DEBUG', trace_exception=True, timeit=True):
    log = logging.getLogger(name)
    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    log_func_map = {
        'DEBUG': log.debug,
        'INFO': log.info,
        'WARNING': log.warning,
        'ERROR': log.error,
        'CRITICAL': log.critical,
    }

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if timeit:
                    begin_time = time.time()

                log.setLevel(log_level_map[level])
                if isinstance(text, str):
                    log_func_map[level](text)

                ret = func(*args, **kwargs)

                if timeit:
                    end_time = time.time()
                    log_func_map[level]("%s(%r, %r) -> %r: %ss" % (func.__name__, args, kwargs, ret, round(end_time-begin_time, 4)))
                else:
                    log_func_map[level]("%s(%r, %r) -> %r" % (func.__name__, args, kwargs, ret))
            except Exception as exc:
                if trace_exception:
                    trace_table(exc)
                if timeit:
                    end_time = time.time()
                    log_func_map[level]("%s(%r, %r) -> %r: %ss" % (func.__name__, args, kwargs, ret, round(end_time-begin_time, 4)))
                else:
                    log_func_map[level]("%s(%r, %r) -> %r" % (func.__name__, args, kwargs, ret))
                raise exc
            else:
                return ret

        return wrapper

    return decorator


@show(level ='DEBUG')
@safe(Exception)
def test(text):
    print(text)
    raise Exception('test')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    ret = test('hello world')
    print(ret, type(ret))
