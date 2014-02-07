'''
Created on Feb 7, 2014

@author: dejan.dezman@cosylab.com
'''
import logging

def _setup_idods_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    #handler = logging.StreamHandler()
    handler = logging.FileHandler('/var/tmp/idods.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
