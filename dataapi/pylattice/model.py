'''
Created on Apr 15, 2013

@author: shengb
'''

import logging

class model(object):
    def __init__(self, conn):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('model')
        hdlr = logging.FileHandler('/var/tmp/model.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)

        self.conn = conn
        
    def retrievemodel(self):
        '''
        '''
        
    def savemodel(self):
        '''
        '''
        
    def updatemodel(self):
        '''
        '''
        
    def retrievegoldmodel(self):
        '''
        '''
        
    def savegoldmodel(self):
        '''
        '''
        
    def updategoldmodel(self):
        '''
        '''
        
    def retrievebeamparameters(self):
        '''
        '''
        
    def savebeamparameters(self):
        '''
        '''
    
    def retrievecloseorbit(self):
        '''
        '''

    def savecloseorbit(self):
        '''
        '''
    
    def retrievetransfermatrix(self):
        '''
        '''

    def savetransfermatrix(self):
        '''
        '''
    
    def retrievetwiss(self):
        '''
        '''

    def savetwiss(self):
        '''
        '''
    
    def retrieveemittance(self):
        '''
        '''

    def saveemittance(self):
        '''
        '''
        
    def savebeamcoordinate(self):
        '''
        '''
        
    def retrievebeamcoordinate(self):
        '''
        '''

    def updatebeamcoordinate(self):
        '''
        '''
        
    
    
    
    