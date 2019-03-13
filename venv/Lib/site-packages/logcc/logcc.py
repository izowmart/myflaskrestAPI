import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep

from loader.dictionary import unpack
from termcc.cc import cc
from termcc.core import blue, yellow, red, cyan, yellow_, bold

from logcc.color_formatter import ColorFormatter


class LogCC:
    def __init__(self, **kwargs):
        self.name, \
        self.color_formatter_config, \
        self.simple_formatter_config, \
        self.console_level, self.logger_level, \
        self.color_theme, \
        self.file_handler, \
        self.netboy_handler, \
        self.sqlite_handler = unpack(kwargs,
                                     ('name', 'default'),
                                     ('color_formatter', {
                                         'fmt': '{asctime} {name} {levelname:8s} {msg}',
                                         'datefmt': '%Y-%m-%d %H:%M:%S',
                                         'style': '{',
                                     }),
                                     ('simple_formatter', {
                                         'fmt': '{asctime} {name} {levelname:8s} {msg}',
                                         'datefmt': '%Y-%m-%d %H:%M:%S',
                                         'style': '{',
                                     }),
                                     ('console_level', logging.DEBUG),
                                     ('logger_level', logging.DEBUG),
                                     ('color_theme', {
                                         # 'user': {
                                         #     'DEBUG': cc(':yin_yang:')
                                         # }
                                     }),
                                     ('file_handler', {
                                         'filename': kwargs.get('logfile', '/tmp/logcc.log'),
                                         'when': 'D',
                                         'interval': 1,
                                         'backupCount': 30
                                     }),
                                     'netboy_handler',
                                     ('sqlite_handler', True)
                                     )

        console = logging.StreamHandler()
        console.setLevel(self.console_level)

        self.color_formatter = ColorFormatter(**self.color_formatter_config)
        for k, theme in self.color_theme.items():
            for l, value in theme.items():
                self.color_formatter.setup_themes(k, l, value)
        console.setFormatter(self.color_formatter)
        logger = logging.getLogger(self.name)

        logger.setLevel(self.logger_level)

        logger.addHandler(console)

        file_handler = TimedRotatingFileHandler(**self.file_handler)
        simple_formatter = logging.Formatter(**self.simple_formatter_config)
        file_handler.setFormatter(simple_formatter)
        logger.addHandler(file_handler)

        if self.netboy_handler:
            from logcc.netboy_handler import NetboyHandler
            h = NetboyHandler(**self.netboy_handler)
            logger.addHandler(h)

        if self.sqlite_handler:
            from logcc.pony_sqlite_handler import PonySQLiteHandler
            h = PonySQLiteHandler()
            logger.addHandler(h)

    def update_color_formatter(self, key, level, value):
        self.color_formatter.setup_themes(key, level, value)


if __name__ == "__main__":
    name = 'test'
    l = LogCC(name=name, logfile='/tmp/test.log')
    l.update_color_formatter('name', 'DEBUG', yellow())
    l.update_color_formatter('name', 'INFO', cc(':blue::yin_yang:'))
    log = logging.getLogger(name)
    while True:
        for i in range(10):
            log.debug('hello')
            log.info('world')
            sleep(1)
        log.debug('\n\n.......................\n\n>>>>>>>>>>>>>>>>>>>>\n\n')
