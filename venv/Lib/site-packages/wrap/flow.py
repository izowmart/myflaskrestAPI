import logging

import functools
from loader.function import load
from logcc.util.table import trace_table


def before(before_func, context=None, block=False, inject=False):
    context = context if context else {}
    before_func = load(before_func) if isinstance(before_func, str) else before_func

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context['args'] = args
            context['kwargs'] = kwargs
            before_ret = before_func(context)
            if block:
                return before_ret
            context['ret'] = before_ret
            if inject:
                kwargs['context'] = context
            ret = func(*args, **kwargs)
            return ret

        return wrapper

    return decorator


def after(after_func, context=None, block=False):
    context = context if context else {}
    after_func = load(after_func) if isinstance(after_func, str) else after_func

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context['args'] = args
            context['kwargs'] = kwargs
            ret = func(*args, **kwargs)

            context['ret'] = ret
            after_ret = after_func(context=context)
            if block:
                return after_ret

            return ret

        return wrapper

    return decorator


# deprecated
def dataflow(before=None, after=None, exception=None, logger='wrap', context=None):
    def decorator(function):

        log = logging.getLogger(logger) if isinstance(logger, str) else logger
        data = {'log': log, 'context': context}

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                data['args'] = args
                data['kwargs'] = kwargs
                before_func = load(before) if isinstance(before, str) else before
                after_func = load(after) if isinstance(after, str) else after
                exception_func = load(exception) if isinstance(exception, str) else exception
                before_ret = function_ret = exception_ret = after_ret = None

                if before_func:
                    log.debug('before handler: {}'.format(function))
                    before_ret = before_func(data)
                    if isinstance(before_ret, dict):
                        block_ret = before_ret.get('block_ret')
                        if block_ret:
                            return block_ret
                try:
                    data['before_ret'] = before_ret
                    function_ret = function(*args, **kwargs)
                except Exception as exc:
                    data['function_ret'] = function_ret
                    if exception_func:
                        data['exception'] = exc
                        exception_ret = exception_func(data)
                        if isinstance(exception_ret, dict):
                            block_ret = exception_ret.get('block_ret')
                            if block_ret:
                                return block_ret
                        trace_table(exc)
                    else:
                        raise exc

                if after_func:
                    log.debug('after handler: {}'.format(function))
                    data['function_ret'] = function_ret
                    data['exception_ret'] = exception_ret
                    after_ret = after_func(data)
                    if isinstance(after_ret, dict):
                        block_ret = after_ret.get('block_ret')
                        if block_ret:
                            return block_ret
                return function_ret

            except Exception as exc:
                trace_table(exc)
                raise Exception('flow wrapper failed!')

        return wrapper

    return decorator


@before(lambda c: (print(c, 'before'), 100)[1], context={'t': 'tt'}, block=True, inject=True)
def test(a, b, context):
    print(context, '.......')
    print(a, b)
    print('========')
    return a + b


@before(lambda c: (print(c, 'before'), 100)[1], context={'t3': 'tt2'}, block=False)
def test2(a, b):
    print(a, b)
    return a + b


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print('.' * 40)
    ans = test(1, 2)
    print('ans: ', ans)
    print('.' * 40)
    ans = test2(1, 2)
    print('ans: ', ans)
