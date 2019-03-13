import logging
import traceback
from textwrap import wrap

from terminaltables import AsciiTable, SingleTable


def grouper_it(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def trace_table(exc, logger='default', note=True, column=5, mode='ascii', level='error', width=40):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    tb = traceback.extract_tb(exc.__traceback__, limit=None)
    len_tb = len(tb)
    group_size = len_tb // column
    if len_tb % column != 0:
        group_size += 1
    if note:
        column -= 1
        if column <= 0:
            column = 1
    for index, tb_chunked in enumerate(grouper_it(tb, column)):
        if note:
            data = [
                ['file'], ['func'], ['desc']
            ]
        else:
            data = [[], [], []]

        for i, frame in enumerate(tb_chunked):
            current_filename = frame.filename
            if i == 0:
                last_filename = frame.filename
            else:
                if current_filename == last_filename:
                    current_filename = ''
                else:
                    last_filename = current_filename  # + ':' + frame.lineno
            if len(current_filename) == 0:
                data[0].append(str(frame.lineno))
            else:
                data[0].append('\n'.join(wrap(current_filename + ':' + str(frame.lineno), width)))
            data[1].append(frame.name)
            data[2].append('\n'.join(wrap(frame.line, width)))

        if mode == 'single':
            table = SingleTable(data, str(group_size) + '-' + str(index + 1))
        else:
            table = AsciiTable(data, str(group_size) + '-' + str(index + 1))

        table.outer_border = True
        table.inner_heading_row_border = True
        table.inner_column_border = True
        table.inner_row_border = True

        # max_width = table.column_max_width(1)
        # wrapped_string = '\n'.join(wrap(LONG_STRING, max_width))
        # table.table_data[0][1] = wrapped_string

        if level == 'critical':
            logger.critical('\n' + table.table)
        elif level == 'warning':
            logger.warning('\n' + table.table)
        elif level == 'info':
            logger.info('\n' + table.table)
        elif level == 'debug':
            logger.debug('\n' + table.table)
        else:
            logger.error('\n' + table.table)


tt = trace_table


def test_3():
    raise Exception('test_3')


def test_2():
    test_3()


def test_1():
    test_2()


def test_0():
    test_1()


def test_m1():
    test_0()


def test_m2():
    test_m1()


if __name__ == '__main__':

    logger = logging.getLogger('test')

    try:
        test_m2()
    except Exception as exc:
        trace_table(exc, 'test', mode='single')
