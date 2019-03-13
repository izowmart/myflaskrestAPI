from datetime import datetime
from logging import Handler

from pony.orm import Database, Required, db_session

db = Database(provider='sqlite', filename='/tmp/logcc.sqlite',  create_db=True)


class Record(db.Entity):
    create_at = Required(datetime, sql_default='CURRENT_TIMESTAMP', default=lambda: datetime.utcnow())
    levelname = Required(str)
    msg = Required(str)
    module = Required(str)
    pathname = Required(str)
    processName = Required(str)
    threadName = Required(str)
    name = Required(str)

    @staticmethod
    @db_session
    def add(levelname, msg, module, pathname, processName, threadName, name):
        Record(levelname=levelname, msg=msg, module=module, pathname=pathname,
               processName=processName, threadName=threadName, name=name)



class PonySQLiteHandler(Handler):
    def __init__(self):
        super(PonySQLiteHandler, self).__init__()
        db.generate_mapping(create_tables=True, check_tables=True)

    def emit(self, record):
        log_entry = self.format(record)
        Record.add(levelname=record.levelname, msg=record.msg, module=record.module, pathname=record.pathname,
                   processName=record.processName, threadName=record.threadName, name=record.name)

        return 'pony sqlite logged'
