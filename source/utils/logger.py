"""Defines a class to encapsulate the ability to log to a database table"""
import time
import logging
from logging.handlers import RotatingFileHandler
import random

SIXTYFOUR_MB = 2**26
THIRTYTWO_MB = 2**25
SIXTEEN_MB = 2**24

class ETL_logger:
    """A class to encapsulate the ability to log"""

    def __init__(self, name, level=logging.INFO):
        LOGFILE = 'ETL'
        logging.basicConfig(filename=LOGFILE, format='%(levelname)s:%(message)s', level=level)
        logfile = RotatingFileHandler(LOGFILE, maxBytes=SIXTEEN_MB, backupCount=20)

        self.logger = logging.getLogger(name)
        self.logger.addHandler(logfile)
        self.id = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=5))

    def log(self, message, level=logging.INFO):
        """Wrapper around self.logger.log .
        Note the order of arguments is different from that in self.logger.log.
        """
        if level == 'error':
            level = logging.ERROR
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logger.log(level, "%s |%s|%s", self.id, now, message)
