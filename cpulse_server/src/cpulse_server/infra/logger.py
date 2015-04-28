import logging.handlers
import inspect
from os import path
import sys

class cpulselog(object):
    ''' Internal Singleton class
        It should be accessed using logger.getlog function '''

    _instance  = None
    def __init__(self, level=logging.DEBUG, logfile='cpulse.log'):
        self.clog = logging.getLogger("%")
        self.clog.setLevel(level)
        self.level = level
        ch = logging.StreamHandler(sys.stdout)
        fh = logging.handlers.RotatingFileHandler(logfile,
                                                  maxBytes=20*1024*1024,
                                                  backupCount=4)
        fh.setLevel(level)

        if level == logging.INFO:
            formatter =logging.Formatter('%(message)s')
        else:
            formatter =logging.Formatter(
                            '%(name)s%(levelname)s-[%(asctime)s]-%(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.clog.addHandler(ch)
        self.clog.addHandler(fh)

    def warn(self, arg):
        frame = inspect.getouterframes(inspect.currentframe())[1]
        msg = path.basename(frame[0].f_code.co_filename)
        msg = msg + ":" +  ( frame[0].f_code.co_name +
                         ":" + str(frame[0].f_lineno) + " " )
        self.clog.warning( msg + arg)

    def err(self, arg):
        frame = inspect.getouterframes(inspect.currentframe())[1]
        msg = path.basename(frame[0].f_code.co_filename)
        msg = msg + ":" +  (frame[0].f_code.co_name +
                 ":" + str(frame[0].f_lineno) + " ")
        if self.level == logging.INFO:
            self.clog.error(arg)
        else:
            self.clog.error( msg + arg)

    def dbg(self, arg):
        frame = inspect.getouterframes(inspect.currentframe())[1]
        msg = path.basename(frame[0].f_code.co_filename)
        msg = msg + ":" +  (frame[0].f_code.co_name +
                 ":" + str(frame[0].f_lineno) + " ")
        self.clog.debug( msg + arg)

    def info(self, arg):
        frame = inspect.getouterframes(inspect.currentframe())[1]
        msg = path.basename(frame[0].f_code.co_filename)
        msg = msg + ":" +  (frame[0].f_code.co_name + ":" +
                         str(frame[0].f_lineno) + " ")
        if self.level == logging.INFO:
            self.clog.info(arg)
        else:
            self.clog.info( msg + arg)

def getlog(level=logging.DEBUG, logfile='vmlog.log'):

    ''' Usage log = logger.getlog()
        log.warn ("Warning messages")
        log.err ("Error messages")
        log.dbg ("Debug messages")
        log.info ("Info messages") '''

    if not cpulselog._instance:
        cpulselog._instance = cpulselog(level,logfile)
    return cpulselog._instance
