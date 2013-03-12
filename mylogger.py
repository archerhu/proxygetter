# -*- coding: utf8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler

class ContextFilter(logging.Filter):
    NAMES = ['gunicorn', 'requests']
    def filter(self, record):
        if record.name is not None and record.name.split(".")[0] in ContextFilter.NAMES:
            return 0
        return 1
    
def loginit(logfile, debug=False):
    if debug:
        loglevel = logging.DEBUG
        logfmt = '%(name)s %(asctime)s [%(process)d] [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    else:
        loglevel = logging.INFO
        logfmt = '%(name)s %(asctime)s [%(process)d] [%(levelname)s] %(message)s'
    log = logging.getLogger()
    fh = TimedRotatingFileHandler(logfile, when='D')
    datefmt = r"%Y-%m-%d %H:%M:%S"
    fh.setFormatter(logging.Formatter(logfmt, datefmt))
    
    f = ContextFilter()  #去除gunicorn的log
    fh.addFilter(f)
    
    log.addHandler(fh)
    log.setLevel(loglevel)
    




