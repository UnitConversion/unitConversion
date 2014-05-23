'''
Tool to time execution of code bocks
@author dejan.dezman@cosylab.com

example of use::

 with Timer() as t:
    code
 print "=> elasped client.saveInsertionDevice: %s s" % t.secs
'''
import time
import logging


class Timer(object):
    def __init__(self, verbose=False, output=" "):
        self.verbose = verbose
        self.output = output
        self.logger = logging.getLogger('timer')
        hdlr = logging.FileHandler('/var/tmp/timer.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        strLog = '=> elapsed time%s: %f ms' % (self.output, self.msecs)
        self.logger.info(strLog)

        if self.verbose:
            print strLog