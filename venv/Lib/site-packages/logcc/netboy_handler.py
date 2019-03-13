from logging import Handler

from netboy.curl.boy import CurlBoy


class NetboyHandler(Handler):
    def __init__(self, url, method):
        super(NetboyHandler, self).__init__()
        self.url = url
        self.method = method

    def emit(self, record):
        log_entry = self.format(record)
        boy = CurlBoy()
        try:
            if self.method == 'post':
                resp = boy.post(self.url, {
                    'levelname': record.levelname,
                    'msg': record.msg,
                    'module': record.module,
                    'pathname': record.pathname,
                    'processName': record.processName,
                    'threadName': record.threadName,
                    'name': record.name
                })
            else:
                resp = boy.get(self.url)
        except Exception as e:
            return 'failed:' + str(type(e)) + ':' + str(e)
        return 'netboy logged'
