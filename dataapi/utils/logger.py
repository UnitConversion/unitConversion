'''
Created on Jun 24, 2013

@author: shengb
'''
import logging

def _setup_logger(name, logfile):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    #handler = logging.StreamHandler()
    handler = logging.FileHandler('/var/tmp/%s'%(logfile))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
