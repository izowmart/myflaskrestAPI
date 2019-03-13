import logging

import functools

from logcc.util.table import trace_table


def async_safe(Exc, trace_exception=True, return_value=None):
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            try:
                ret = await function(*args, **kwargs)
            except Exc as exc:
                if trace_exception:
                    trace_table(exc)
                if return_value is not None:
                    return return_value
                return exc
            return ret

        return wrapper

    return decorator

def safe(Exc, trace_exception=True, return_value=None):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                ret = function(*args, **kwargs)
            except Exc as exc:
                if trace_exception:
                    trace_table(exc)
                if return_value is not None:
                    return return_value
                return exc
            return ret

        return wrapper

    return decorator



@safe(Exception)
def test(text):
    print(text)
    raise Exception('test')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    ret = test('hello world')
    print(ret, type(ret))
