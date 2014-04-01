'''
Created on Apr 15, 2013

@author: shengb
'''

from collections import OrderedDict

import logging
import MySQLdb

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from .lattice import lattice

from utils import _wildcardformat

class model(object):
    def __init__(self, conn, lat=None, transaction=None):
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
        self.lat=lat
        
        # use django transaction management
        self.transaction = transaction
        if self.lat == None:
            self.lat=lattice(self.conn, transaction=self.transaction)

    def savemodelcodeinfo(self, codename, algorithm):
        '''
        save simulation code which could be used to carry out one particular run with given lattice.
        The code name, and its algorithm are capture.
        parameter:
            codename: simulation code name, elegant or tracy for example
            algorithm: algorithm to be use to generate the beam parameters such as TWISS, and close orbit.
        
        Return: model code id if success, other raise an exception.
        '''
        res = self.retrievemodelcodeinfo(codename, algorithm)
        if len(res) != 0:
            raise ValueError ('Entry exists already for model code (%s) with algorithm (%s)'%(codename, algorithm))
        sql = '''
        insert into model_code
        (code_name, algorithm)
        value
        (%s, %s)
        '''
        try:
            cur=self.conn.cursor()
            cur.execute(sql, (codename, algorithm))
            modelcodeid = cur.lastrowid
            if self.transaction:
                    self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving a new model code info:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving a new model code info:\n%s (%d)' %(e.args[1], e.args[0]))
        return modelcodeid
        
    def retrievemodelcodeinfo(self, codename, algorithm):
        '''
        retrieve model code information with given name and algorithm
        Wildcasts are supported for search in code name and algorithm.
            * for multiple characters matching
            ? for single character matching
            
        return tuple of model code id, model code name, and algorithm
        '''
        sql = '''
        select model_code_id, code_name, algorithm
        from model_code
        where
        '''
        if  "*" in codename or "?" in codename:
            sql += 'code_name like %s '
            codename = _wildcardformat(codename)
        else:
            sql += 'code_name = %s '
        if algorithm:
            if algorithm == "*":
                pass
            elif "*" in algorithm or "?" in algorithm:
                sql += 'and algorithm like %s'
                algorithm = _wildcardformat(algorithm)
            else:
                sql += 'and algorithm = %s'
        else:
            sql += ' and algorithm is NULL'
        
        try:
            cur = self.conn.cursor()
            if algorithm==None or algorithm == "*":
                cur.execute(sql, (codename,))
            else:
                cur.execute(sql, (codename, algorithm))
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving model code info:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving model code info:\n%s (%d)' %(e.args[1], e.args[0]))
        return res
    
    def retrievemodellist(self, latticename, latticebranch=None, latticeversion=None):
        '''
        Retrieve a model list that satisfies given constrains.
        parameters:
            latticename:    lattice name that this model belongs to
            latticeversion: the version of lattice
            latticebranch:  the branch of lattice
            
        
        return: a dictionary
                {'model name':                            # model name
                               {'id': ,                   # model id number
                                'latticeId': ,            # id of the lattice which given model belongs to
                                'description': ,          # description of this model
                                'creator': ,              # name who create this model first time
                                'originalDate': ,         # date when this model was created
                                'updated': ,              # name who modified last time
                                'lastModified': ,         # the date this model was modified last time
                               }
                 ...
                }
        '''
        sql = '''
        select model_id, lattice_id, 
               model_name, model_desc, 
               created_by, create_date,
               updated_by, update_date
        from model
        left join model_code on model_code.model_code_id = model.model_code_id
        where
        lattice_id = %s
        '''
        lattices = self.lat.retrievelatticeinfo(latticename, version=latticeversion, branch=latticebranch)
        resdict = {}
        
        for latticeid, _ in lattices.iteritems():
            try:
                cur = self.conn.cursor()
                cur.execute(sql, (latticeid,))
                results=cur.fetchall()
                for res in results:
                    resdict[res[2]] = {'id': res[0],
                                       'latticeid': res[1],
                                       }
                    if res[3]!=None:
                        resdict[res[2]]['description'] = res[3]
                    if res[4]!=None:
                        resdict[res[2]]['creator'] = res[4]
                    if res[5]!=None:
                        resdict[res[2]]['originalDate'] = res[5].isoformat()
                    if res[6]!=None:
                        resdict[res[2]]['updated'] = res[6]
                    if res[7]!=None:
                        resdict[res[2]]['lastModified'] = res[7].isoformat()
            except MySQLdb.Error as e:
                self.logger.info('Error when retrieving model code info:\n%s (%d)' %(e.args[1], e.args[0]))
                raise Exception('Error when retrieving model code info:\n%s (%d)' %(e.args[1], e.args[0]))
        return resdict
    
    def retrievemodel(self, modelname=None, modelid=None):
        '''
        Retrieve a model list with global parameters such as tune & chromaticity that satisfies given constrains.
        parameters:
            modelname:      the name shows that which model this API will deal with
            modelid:        the id shows that which model this API will deal with
        
        return: a dictionary
                {'id':                                    # model name
                               {'id': ,                   # model id number
                                'latticeId': ,            # id of the lattice which given model belongs to
                                'name': ,                 # model name
                                'description': ,          # description of this model
                                'creator': ,              # name who create this model first time
                                'originalDate': ,         # date when this model was created
                                'updated': ,              # name who modified last time
                                'lastModified': ,         # the date this model was modified last time
                                'tunex': ,                # horizontal tune
                                'tuney': ,                # vertical tune
                                'alphac': ,               # momentum compaction
                                'chromX0': ,             # linear horizontal chromaticity
                                'chromX1': ,             # non-linear horizontal chromaticity
                                'chromX2': ,             # high order non-linear horizontal chromaticity
                                'chromY0': ,             # linear vertical chromaticity
                                'chromY1': ,             # non-linear vertical chromaticity
                                'chromY2': ,             # high order non-linear vertical chromaticity
                                'finalEnergy': ,          # the final beam energy in GeV
                                'simulationCode': ,       # name of simulation code, Elegant and Tracy for example
                                'sumulationAlgorithm': ,  # algorithm used by simulation code, for example serial or parallel,
                                                          # and SI, or SI/PTC for Tracy code
                                'simulationControl': ,    # various control constrains such as initial condition, beam distribution, 
                                                          # and output controls
                                'simulationControlFile':  # file name that control the simulation conditions, like a .ele file for elegant
                               }
                 ...
                }
        '''
        if modelname==None and modelid==None:
            raise ValueError("Cannot identify a model since neither name nor id is provided.")
        sql = '''
        select model_id, lattice_id, 
               model_name, model_desc, 
               created_by, create_date,
               updated_by, update_date,
               tune_x, tune_y, alphac,
               chrome_x_0, chrome_x_1, chrome_x_2,
               chrome_y_0, chrome_y_1, chrome_y_2,
               final_beam_energy,
               code_name, algorithm, 
               model_control_data, model_control_name
        from model
        left join model_code on model_code.model_code_id = model.model_code_id
        where
        '''
        vals=[]
        modelname = str(modelname)
        if isinstance(modelid, (str, unicode)):
            modelid=str(modelid)
        if modelname != None and modelid != None:
            if "*" in modelname or "?" in modelname:
                sql += ' model_name like %s'
                vals.append(_wildcardformat(modelname))
            else:
                sql += ' model_name = %s'
                vals.append(modelname)
            
            if "*" in modelid or "?" in modelid:
                sql += ' and model_id like %s'
                vals.append(_wildcardformat(modelid))
            else:
                sql += ' and model_id = %s'
                vals.append(modelid)
        elif modelname !=None:
            if "*" in modelname or "?" in modelname:
                sql += ' model_name like %s'
                vals.append(_wildcardformat(modelname))
            else:
                sql += ' model_name = %s'
                vals.append(modelname)
        else:
            sql += ' model_id = %s'
            vals.append(modelid)

#        modelname = _wildcardformat(modelname)
        modelres = {}
        try:
            cur=self.conn.cursor()
            
            cur.execute(sql, vals)
            results = cur.fetchall()
            
            for res in results:
                tempdict = {'id': res[0],
                            'latticeId': res[1],
                            'name': res[2]}
                keys=['description', 'creator', 'originalDate',
                      'updated', 'lastModified',
                      'tunex', 'tuney', 'alphac',
                      'chromX0', 'chromX1', 'chromX2',
                      'chromY0', 'chromY1', 'chromY2',
                      'finalEnergy', 
                      'simulationCode', 'sumulationAlgorithm',
                      'simulationControl', 'simulationControlFile'
                      ]
                for i in range(3, len(res)):
                    if res[i] != None:
                        if keys[i-3] in ['originalDate', 'lastModified']:
                            tempdict[keys[i-3]] = res[i].isoformat()
                        else:
                            tempdict[keys[i-3]] = res[i]
                
                modelres[res[0]]=tempdict
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving model information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving model information:\n%s (%d)' %(e.args[1], e.args[0]))
        
        return modelres

    def _elementslist2dict(self, elements):
        elementinfo = {}
        for element in elements:
            elementinfo[str(element[2])] = {'id': element[0], 'name': element[1]}
        return elementinfo
    
    def _savebeamparameters(self, cursor, latticeid, modelid, beamparameter):
        '''
        beamparameter is a dictionary which hosts all beam simulation results.
            { element_order: #element_order starts with 0, which is the begin of simulation with s=0.
                { 'name': ,
                  'position': ,
                  'alphax': ,
                  'alphay': ,
                  'betax': ,
                  'betay': ,
                  'etax': ,
                  'etay': ,
                  'etapx': ,
                  'etapy': ,
                  'phasex': ,
                  'phasey': ,
                  'codx': ,
                  'cody': ,
                  'transferMatrix': ,
                  'indexSliceCheck': ,
                  's': ,
                  'energy': ,
                  'particleSpecies': ,
                  'particleMass': ,
                  'particleCharge': ,
                  'beamChargeDensity': ,
                  'beamCurrent': ,
                  'x': ,
                  'xp': ,
                  'y': ,
                  'yp': ,
                  'z': ,
                  'zp': ,
                  'emittancex': ,
                  'emittancey': ,
                  'emittancexz':  
                }
            }
        '''
        if len(beamparameter) == 0:
            # nothing to do with empty data
            return
        elements = self.lat._retrieveelementbylatticeid(latticeid, cursor)
        elementinfo = self._elementslist2dict(elements)

        #sql = '''insert into beam_parameter
        sqlhead = '''insert into beam_parameter
        (model_id, element_id, 
        pos, 
        alpha_x, alpha_y, 
        beta_x, beta_y, 
        eta_x, eta_y,
        etap_x, etap_y,
        nu_x, nu_y,
        co_x, co_y,
        index_slice_chk,
        s,
        energy, 
        particle_species,
        particle_mass,
        particle_charge,
        beam_charge_density,
        beam_current,
        x, xp,
        y, yp,
        z, zp,
        emit_x, emit_y, emit_z,
        transfer_matrix)
        values
        '''
        
        for bpkey, bpval in beamparameter.iteritems():
            # bpkey is element order
            # bpval is element beam parameter result
            if elementinfo.has_key(bpkey):
                elementid = elementinfo[bpkey]['id']
                elementname = elementinfo[bpkey]['name']
                
                # check whether the element name matches that in element
                if elementname.upper() != bpval['name'].upper() and bpkey != 0:
                    raise ValueError('Element name (%s) does not match that in lattice (%s).'
                                     %(bpval['name'], elementname))
                sql = sqlhead + '(%s, %s, '
                sqlval = [modelid, elementid]
                #sql += '(%s, %s, '%(modelid, elementid)
                for key in ['position', 
                            'alphax', 'alphay', 'betax', 'betay', 'etax', 'etay', 'etapx', 'etapy', 'phasex', 'phasey',
                            'codx', 'cody',
                            'indexSliceCheck',
                            's',
                            'energy',
                            'particleSpecies',
                            'particleMass',
                            'particleCharge',
                            'beamChargeDensity',
                            'beamCurrent',
                            'x', 'xp', 'y', 'yp', 'z', 'zp',
                            'emittancex', 'emittancey', 'emittancexz',
                            'transferMatrix']:
                    if bpval.has_key(key):
                        sql += '%s, '
                        if key == 'transferMatrix':
                            #sql += '"%s", '%(json.dumps(bpval[key]))
                            sqlval.append(json.dumps(bpval[key]))
                        else:
                            #sql += '%s, '%(bpval[key])
                            sqlval.append(bpval[key])
                    else:
                        sql += 'NULL, '
                #sql= sql[:-2]+'),'
                sql= sql[:-2]+')'
                cursor.execute(sql, sqlval)
            else:
                raise ValueError('elements in lattice do not match that in model')
        #cursor.execute(sql[:-1])

    def _updatebeamparameters(self, cursor, latticeid, modelid, beamparameter):
        '''
        beamparameter is a dictionary which hosts all beam simulation results.
            { element_order: 
                { 'name': ,
                  'pos': ,
                  'alphax': ,
                  'alphay': ,
                  'betax': ,
                  'betay': ,
                  'etax': ,
                  'etay': ,
                  'etapx': ,
                  'etapy': ,
                  'phasex': ,
                  'phasey': ,
                  'cox': ,
                  'coy': ,
                  'transferMatrix': ,
                  'indexSliceCheck': ,
                  's': ,
                  'energy': ,
                  'particleSpecies': ,
                  'particleMass': ,
                  'particleCharge': ,
                  'beamChargeDensity': ,
                  'beamCurrent': ,
                  'x': ,
                  'xp': ,
                  'y': ,
                  'yp': ,
                  'z': ,
                  'zp': ,
                  'emittancex': ,
                  'emittancey': ,
                  'emittancexz':  
                }
            }
        '''
        if len(beamparameter) == 0:
            # nothing to do with empty data
            return
        elements = self.lat._retrieveelementbylatticeid(latticeid, cursor)
        elementinfo = self._elementslist2dict(elements)
        
        for bpkey, bpval in beamparameter.iteritems():
            sql = '''update beam_parameter set '''
            # bpkey is element order
            # bpval is element beam parameter result
            
            if elementinfo.has_key(bpkey):
                elementid = elementinfo[bpkey]['id']
                elementname = elementinfo[bpkey]['name']
                
                # check whether the element name matches that in element
                if elementname.upper() != bpval['name'].upper() and bpkey != 0:
                    raise ValueError('Element name (%s) does not match that in lattice (%s).'
                                     %(bpval['name'], elementname))
                # map key to database table column names
                keyvals = {'pos': 'pos',
                           'alphax': 'alpha_x',
                           'alphay': 'alpha_y',
                           'betax': 'beta_x',
                           'betay': 'beta_y',
                           'etax': 'eta_x',
                           'etay': 'eta_y',
                           'etapx': 'etap_x',
                           'etapy': 'etap_y',
                           'phasex': 'nu_x',
                           'phasey': 'nu_y',
                           'cox': 'co_x',
                           'coy': 'co_y',
                           'transferMatrix': 'transfer_matrix',
                           'indexSliceCheck': 'index_slice_chk',
                           's': 's',
                           'energy': 'energy',
                           'particleSpecies': 'particle_cpecies',
                           'particleMass': 'particle_mass',
                           'particleCharge': 'particle_charge',
                           'beamChargeDensity': 'beam_charge_density',
                           'beamCurrent': 'beam_current',
                           'x': 'x',
                           'xp': 'xp',
                           'y': 'y',
                           'yp': 'yp',
                           'z': 'z',
                           'zp': 'zp',
                           'emittancex': 'emit_x',
                           'emittancey': 'emit_y',
                           'emittancexz': 'emit_z'
                }
                for k, v in keyvals.iteritems():
                    if bpval.has_key(k):
                        sql += '%s = %s,'%(v, bpval[k])
            else:
                raise ValueError('elements in lattice do not match that in model')
            sql = sql[:-1] +' where element_id = %s'%elementid
            cursor.execute(sql)
        
    def savemodel(self, model, latticename, latticeversion, latticebranch, defaultuser=None):
        '''
        Save a model.
        parameters:
            latticename:    lattice name that this model belongs to
            latticeversion: the version of lattice
            latticebranch:  the branch of lattice
            
            model:          a dictionary which holds all data 
                {'model name':                            # model name
                               { # header information
                                'description': ,          # description of this model
                                'creator': ,              # name who create this model first time
                                'updated': ,              # name who modified last time
                                'tunex': ,                # horizontal tune
                                'tuney': ,                # vertical tune
                                'alphac':                 # momentum compaction factor
                                'chromX0': ,             # linear horizontal chromaticity
                                'chromX1': ,             # non-linear horizontal chromaticity
                                'chromX2': ,             # high order non-linear horizontal chromaticity
                                'chromY0': ,             # linear vertical chromaticity
                                'chromY1': ,             # non-linear vertical chromaticity
                                'chromY2': ,             # high order non-linear vertical chromaticity
                                'finalEnergy': ,          # the final beam energy in GeV
                                'simulationCode': ,       # name of simulation code, Elegant and Tracy for example
                                'sumulationAlgorithm': ,  # algorithm used by simulation code, for example serial or parallel,
                                                          # and SI, or SI/PTC for Tracy code
                                'simulationControl': ,    # various control constrains such as initial condition, beam distribution, 
                                                          # and output controls
                                'simulationControlFile':  # file name that control the simulation conditions, like a .ele file for elegant
                                
                                # simulation data
                                'beamParameter':          # a dictionary consists of twiss, close orbit, transfer matrix and others
                               }
                 ...
                }
        
        Use updatemodel() instead if a model exists already.
        Simulation info (simulationCode, simulationAlgorithm) has to been provided to enable updatemodel() later.
        
        return: model id if success, otherwise raise a ValueError exception
        '''
        modelids = []
        for modelname, modeldata in model.iteritems():
            # check whether a model exists already.
            results = self.retrievemodel(modelname=modelname)
            if len(results) != 0:
                raise ValueError('Model (%s) for given lattice (name: %s, version: %s, branch: %s) exists already.'
                                 %(modelname, latticename, latticeversion, latticebranch))
            lattices = self.lat.retrievelatticeinfo(latticename, version=latticeversion, branch=latticebranch)
            
            if not modeldata.has_key('creator') and defaultuser != None:
                modeldata['creator'] = defaultuser
            
            if len(lattices) == 0:
                raise ValueError('lattice (name: %s, version: %s, branch: %s) does not exist yet.'
                                 %(latticename, latticeversion, latticebranch))
            for latticeid, _ in lattices.iteritems():
                #latticeid = v['id']
                if modeldata.has_key('simulationCode'):
                    simulationcode = modeldata['simulationCode']
                else:
                    simulationcode = None
                if modeldata.has_key('sumulationAlgorithm'):
                    simulationalgorithm = modeldata['sumulationAlgorithm']
                else:
                    simulationalgorithm = None
                
                sql = 'insert into model (lattice_id, model_name, '
                sqlval = 'values (%s, %s, '
                vals = [latticeid, modelname]
                # check whether simulation code info is provided
                if simulationcode != None:
                    # has simulation code info, get the ID
                    modelcode = self.retrievemodelcodeinfo(simulationcode, simulationalgorithm)
                    if len(modelcode) == 0:
                        # simulation code info does not exist. Save a new entry
                        modelcodeid = self.savemodelcodeinfo(simulationcode, simulationalgorithm)
                    else:
                        # find simulation code info.
                        # since it should be unique, get the first as ID.
                        # Save a new entry
                        modelcodeid = modelcode[0][0]
                    sql += ' model_code_id,'
                    vals.append(modelcodeid)
                    sqlval += '%s, '

                # save other attributes
                keys = {'description': 'model_desc',
                        'tunex': 'tune_x',
                        'tuney': 'tune_y',
                        'chromX0': 'chrome_x_0',
                        'chromX1': 'chrome_x_1',
                        'chromX2': 'chrome_x_2',
                        'chromY0': 'chrome_y_0',
                        'chromY1': 'chrome_y_1',
                        'chromY2': 'chrome_y_2',
                        'alphac':  'alphac',
                        'alphac2': 'alphac2',
                        'finalEnergy': 'final_beam_energy',
                        'simulationControl': 'model_control_data',
                        'simulationControlFile': 'model_control_name',
                        'creator': 'created_by'
                }
                for k, v in keys.iteritems():
                    if modeldata.has_key(k):
                        sql += ' %s,' %v
                        if k == 'simulationControl':
                            vals.append(json.dumps(modeldata[k]))
                        else:
                            vals.append(modeldata[k])
                        sqlval += ' %s, '
                sql += ' create_date) '
                sqlval += ' now() )'
                sql += sqlval
                try:
                    cur=self.conn.cursor()
                    cur.execute(sql, vals)
                    
                    modelid=cur.lastrowid
                    if modeldata.has_key('beamParameter'):
                        self._savebeamparameters(cur, latticeid, modelid, modeldata['beamParameter'])
                    if self.transaction:
                        self.transaction.commit_unless_managed()
                    else:
                        self.conn.commit()
                except MySQLdb.Error as e:
                    if self.transaction:
                        self.transaction.rollback_unless_managed()
                    else:
                        self.conn.rollback()
                    self.logger.info('Error when saving a model:\n%s (%d)' %(e.args[1], e.args[0]))
                    raise Exception('Error when saving a model:\n%s (%d)' %(e.args[1], e.args[0]))
            modelids.append(modelid)    
        return modelids

    def updatemodel(self, model, latticename, latticeversion, latticebranch):
        '''
        update an existing model.
        parameters:
            model:          a dictionary which holds all data 
                {'model name':                            # model name
                               { # header information
                                'description': ,          # description of this model
                                'tunex': ,                # horizontal tune
                                'tuney': ,                # vertical tune
                                'chromX0': ,              # linear horizontal chromaticity
                                'chromX1': ,              # non-linear horizontal chromaticity
                                'chromX2': ,              # high order non-linear horizontal chromaticity
                                'chromY0': ,              # linear vertical chromaticity
                                'chromY1': ,              # non-linear vertical chromaticity
                                'chromY2': ,              # high order non-linear vertical chromaticity
                                'finalEnergy': ,          # the final beam energy in GeV
                                'simulationCode': ,       # name of simulation code, Elegant and Tracy for example
                                'sumulationAlgorithm': ,  # algorithm used by simulation code, for example serial or parallel,
                                                          # and SI, or SI/PTC for Tracy code
                                'simulationControl': ,    # various control constrains such as initial condition, beam distribution, 
                                                          # and output controls
                                'simulationControlFile':  # file name that control the simulation conditions, like a .ele file for elegant
                                
                                # simulation data
                                'beamParameter':          # a dictionary consists of twiss, close orbit, transfer matrix and others
                               }
                 ...
                }
            latticename:    lattice name that this model belongs to
            latticeversion: the version of lattice
            latticebranch:  the branch of lattice
        
        Use savemodel() instead if a model does not exist yet.
        Simulation info has to be provided and matches those inside the existing model.
        Otherwise, raise an exception.
        
        return: True if success, otherwise raise a ValueError exception
        '''
        for modelname, modeldata in model.iteritems():
            # check whether a model exists already.
            results = self.retrievemodel(modelname, latticename=latticename, latticeversion=latticeversion, latticebranch=latticebranch)
            if len(results) != 1:
                raise ValueError('Cannot find model (%s) for given lattice (name: %s, version: %s, branch: %s), or more than one found.'
                                 %(modelname, latticename, latticeversion, latticebranch))
            results = results[modelname]
            modelid = results['id']
            latticeid = results['latticeId']
            if modeldata.has_key('simulationCode'):
                simulationcode = modeldata['simulationCode']
            else:
                simulationcode = None
            if modeldata.has_key('sumulationAlgorithm'):
                simulationalgorithm = modeldata['sumulationAlgorithm']
            else:
                simulationalgorithm = None
            
            # check whether model info (code and algorithm) matches with those of existing model
            if simulationcode == None or simulationalgorithm == None:
                raise ValueError('Unknown simulation code or algorithm. Cannnot update a existing model.')
            else:
                modelinfo = self.retrievemodelcodeinfo(simulationcode, simulationalgorithm)
                if len(modelinfo) == 1:
                    modelinfo = modelinfo[0]
                    
                    if modelinfo[1] != simulationcode:
                        # the results are from different simulation code. 
                        # can not update
                        raise ValueError('Simulation code (code: %s) does not match with a existing model (code: %s).'
                                         %(simulationcode, modelinfo[1]))
                    elif modelinfo[2]:
                        # simulation algorithm is not empty
                        if simulationalgorithm != modelinfo[2]:
                            # algorithm does not match each other
                            # results were from different algorithms
                            raise ValueError('Simulation algorithm (algorithm: %s) does not match with a existing model (algorithm: %s).'
                                             %(simulationalgorithm, modelinfo[2]))
                    else:
                        # simulation algorithm is not available. Can not update.
                        raise ValueError('Simulation algorithm (algorithm: %s) does not match with a existing model (algorithm: %s).'
                                         %(simulationalgorithm, modelinfo[2]))
                elif len(modelinfo) == 0:
                    # simulation code info does not exist.
                    # Cannot update an existing model.
                    raise ValueError('Cannot find model info (code: %s, algorithm: %s). Failed to update a model.'
                                     %(simulationcode, simulationalgorithm))
                else:
                    # more than one entry found for given simulation code with its algorithm
                    raise ValueError('Given model info is not unique (code: %s, algorithm: %s).'
                                     %(simulationcode, simulationalgorithm))
            
            sql = 'update model SET '
            keys = {'description': 'model_desc',
                    'tunex': 'tune_x',
                    'tuney': 'tune_y',
                    'chromX0': 'chromme_x_0',
                    'chromX1': 'chromme_x_1',
                    'chromX2': 'chromme_x_2',
                    'chromY0': 'chromme_y_0',
                    'chromY1': 'chromme_y_1',
                    'chromY2': 'chromme_y_2',
                    'alphac':  'alphac',
                    'alphac2': 'alphac2',
                    'finalEnergy': 'final_beam_energy',
                    'simulationControl': 'model_control_data',
                    'simulationControlFile': 'model_control_name',
                    'creator': 'updated_by'
            }

            for k, v in keys.iteritems():
                if modeldata.has_key(k):
                    sql += ' %s = "%s",' %(v, modeldata[k])
            sql += ' update_date = now() where model_id = %s'%modelid
            try:
                cur=self.conn.cursor()
                cur.execute(sql)
                if modeldata.has_key('beamParameter'):
                    self._updatebeamparameters(cur, 
                                               latticeid, 
                                               modelid, 
                                               modeldata['beamParameter'])
                if self.transaction:
                    self.transaction.commit_unless_managed()
                else:
                    self.conn.commit()
            except MySQLdb.Error as e:
                if self.transaction:
                    self.transaction.rollback_unless_managed()
                else:
                    self.conn.rollback()
                self.logger.info('Error when updating a model:\n%s (%d)' %(e.args[1], e.args[0]))
                raise Exception('Error when updating a model:\n%s (%d)' %(e.args[1], e.args[0]))
        return True
        
    def retrievegoldenmodel(self, name, status=0, ignorestatus=False):
        '''
        Retrieve golden model with given name and other conditions
        parameters:
            name:    model name
            status:  0: current golden model [by default]
                     1: alternative golden model
                     2: previous golden models, but not any more
            ignorestatus: get golden model no matter its status
        '''
        name = _wildcardformat(name)
        sql = '''
        select gold_model_id, model_name, 
               gm.created_by, gm.create_date,
               gm.updated_by, gm.update_date,
               gm.gold_status_ind, gm.model_id
        from gold_model gm
        left join model on model.model_id = gm.model_id
        where
        model.model_name like %s
        '''
        try:
            cur=self.conn.cursor()
            if ignorestatus:
                cur.execute(sql, (name, ))
            else:
                cur.execute(sql+''' and gm.gold_status_ind like %s''', (name, status))
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving golden model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving golden model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
        
        return res
    
    def savegoldenmodel(self, name, status=0, creator=None):
        '''
        Save a model to a golden model
        Parameters:
            name:    model name
            creator: who craeted it, or changed the status last time
            status:  0: current golden model [by default]
                     1: alternative golden model
                     2: previous golden models, but not any more
                     other number can be defined by user
        
        return: True if saving gold model successfully, otherwise, raise an exception
        '''
        creator = _wildcardformat(creator)
        sql = '''select model_id from model where model_name = %s'''
        cur=self.conn.cursor()
        
        try:
            # get model id with given model name
            cur.execute(sql, (_wildcardformat(name),))
            res=cur.fetchall()
            if len(res) != 1:
                raise ValueError('Error when retrieving model id for model (%s).'%name)
            else:
                modelid = res[0][0]
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))

        res = self.retrievegoldenmodel(name, ignorestatus=True)
        if len(res) == 0:
            # if not found, flag model with given status.
            # by default, flag it as current golden model
            if creator == None:
                sql = '''
                insert into gold_model
                (model_id, created_by, create_date, gold_status_ind)
                values
                (%s, NULL, now(), %s)
                '''
                vals=(modelid, status)
            else:
                sql = '''
                insert into gold_model
                (model_id, created_by, create_date, gold_status_ind)
                values
                (%s, %s, now(), %s)
                '''
                vals=(modelid, creator, status)
        elif len(res) == 1:
            if creator == None:
                sql = '''
                update gold_model
                set gold_status_ind = %s, updated_by=NULL, update_date = now()
                where gold_model_id = %s 
                '''
                vals = (status, res[0][0])
            else:
                sql = '''
                update gold_model
                set gold_status_ind = %s, updated_by = %s, update_date = now()
                where gold_model_id = %s 
                '''
                vals = (status, creator, res[0][0])
        else:
            raise ValueError('More than one golden model found for given model (name: %s)'
                             %(name))
        try:
            cur.execute(sql, vals)
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
                
            self.logger.info('Error when saving golden model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when saving golden model:\n%s (%d)' 
                             %(e.args[1], e.args[0]))

        return True
    
    def retrieveclosedorbit(self, params):
        '''
        Retrieve closed orbit that satisfies given constrains.
        parameters:
            modelname:   the name shows that which model this API will deal with
            from:        s position of starting element, default 0
            to:          s position of ending element, default the max of element in a lattice
        
        return: a dictionary
                {'model name':  # model name
                    {
                        'name': [element name],
                        'index': [element index],
                        'position': [s position],
                        'codx': [codx],
                        'cody': [cody]
                    }
                 ...
                }
        '''
        if params.has_key('modelname'):
            name=params['modelname']
        else:
            raise TypeError('Not model name specified.')
        if params.has_key('from'):
            start = float(str(params['from']))
        else:
            start = None
        if params.has_key('to'):
            end = float(str(params['to']))
        else:
            end = None
        
        sql = '''
        select model.model_id, model_name, element_name, element_order, bp.pos, element.s, co_x, co_y
        from model
        left join lattice on lattice.lattice_id = model.lattice_id
        left join element on element.lattice_id = lattice.lattice_id
        left join beam_parameter bp on bp.element_id = element.element_id and bp.model_id = model.model_id
        where model_name
        '''
        sqlvals = []
        if "*" in name or "%" in name:
            name = _wildcardformat(name)
            sql += " like %s "
        else:
            sql += " = %s "
        sqlvals.append(name)
        if start != None and end != None:
            sql += ' and element.s between %s and %s '
            sqlvals.append(start)
            sqlvals.append(end)
        elif start != None:
            sql += ' and element.s >= %s '
            sqlvals.append(start)
        elif end != None:
            sql += ' and element.s <= %s '
            sqlvals.append(end)

        try:
            sql += " order by bp.pos "
            cur=self.conn.cursor()
            cur.execute(sql, sqlvals)
            results = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving closed orbit:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving closed orbit:\n%s (%d)'
                             %(e.args[1], e.args[0]))
        
        resdict = OrderedDict()
        if len(results) != 0:
            modelid = results[0][0]
            modelname = results[0][1]
            ename = []
            order = []
            pos = []
            codx = []
            cody = []
            for res in results:
                if modelid == res[0] and modelname == res[1]:
                    ename.append(res[2])
                    order.append(res[3])
                    pos.append(res[4])
                    codx.append(res[6])
                    cody.append(res[7])
                else:
                    # when retrieving 
                    resdict[modelname] = {'name': ename,
                                          'index': order,
                                          'position': pos,
                                          'codx': codx,
                                          'cody': cody}
                    modelid = results[0][0]
                    modelname = results[0][1]
                    ename = []
                    order = []
                    pos = []
                    codx = []
                    cody = []
                # save last value
                resdict[modelname] = {'name': ename,
                                      'order': order,
                                      'position': pos,
                                      'codx': codx,
                                      'cody': cody}

        return resdict
        
    def retrievetransfermatrix(self, params):
        '''
        Retrieve transfer matrix that satisfies given constrains.
        parameters:
            modelname:   the name shows that which model this API will deal with
            from:        index of starting element
            to:          index of ending element
        
        return: a dictionary
                {'model name':  # model name
                    {
                        'name': [element name],
                        'index': [element index],
                        'position': [s position],
                        'transferMatrix':[[transfer matrix],],
                    }
                 ...
                }
        '''
        if params.has_key('modelname'):
            name=params['modelname']
        else:
            raise TypeError('Not model name specified.')
        if params.has_key('from'):
            start = float(str(params['from']))
        else:
            start = None
        if params.has_key('to'):
            end = float(str(params['to']))
        else:
            end = None
        
        sql = '''
        select model.model_id, model_name, element_name, element_order, bp.pos, element.s, transfer_matrix
        from model
        left join lattice on lattice.lattice_id = model.lattice_id
        left join element on element.lattice_id = lattice.lattice_id
        left join beam_parameter bp on bp.element_id = element.element_id and bp.model_id = model.model_id
        where model_name
        '''
        sqlvals = []
        if "*" in name or "%" in name:
            name = _wildcardformat(name)
            sql += " like %s "
        else:
            sql += " = %s "
        sqlvals.append(name)
        if start != None and end != None:
            sql += ' and element.s between %s and %s '
            sqlvals.append(start)
            sqlvals.append(end)
        elif start != None:
            sql += ' and element.s >= %s '
            sqlvals.append(start)
        elif end != None:
            sql += ' and element.s <= %s '
            sqlvals.append(end)

        try:
            sql += " order by bp.pos "
            cur=self.conn.cursor()
            cur.execute(sql, sqlvals)
            results = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving closed orbit:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving closed orbit:\n%s (%d)'
                             %(e.args[1], e.args[0]))
        
        resdict = OrderedDict()
        if len(results) != 0:
            modelid = results[0][0]
            modelname = results[0][1]
            ename = []
            order = []
            pos = []
            tmat = []
            for res in results:
                if modelid == res[0] and modelname == res[1]:
                    ename.append(res[2])
                    order.append(res[3])
                    pos.append(res[4])
                    tmat.append(json.loads(res[6]))
                else:
                    # when retrieving 
                    resdict[modelname] = {'name': ename,
                                          'index': order,
                                          'position': pos,
                                          'transferMatrix': tmat}
                    modelid = results[0][0]
                    modelname = results[0][1]
                    ename = []
                    order = []
                    pos = []
                    tmat = []
                # save last value
                resdict[modelname] = {'name': ename,
                                      'order': order,
                                      'position': pos,
                                      'transferMatrix': tmat}

        return resdict
    
    def retrievetwiss(self, params):
        '''
        Retrieve twiss parameters that satisfies given constrains.
        parameters:
            modelname:   the name shows that which model this API will deal with
            from:        index of starting element
            to:          index of ending element
        
        return: a dictionary
                {'model name':  # model name
                    {
                        'name': [element name],
                        'index': [element index],
                        'position': [s position],
                        'alphax': [],
                        'alphay': [],
                        'betax':  [],
                        'betay':  [],
                        'etax':   [],
                        'etay':   [],
                        'etapx':  [],
                        'etapy':  [],
                        'phasex': [],
                        'phasey': [],
                    }
                 ...
                }
        '''
        if params.has_key('modelname'):
            name=params['modelname']
        else:
            raise TypeError('Not model name specified.')
        if params.has_key('from'):
            start = float(str(params['from']))
        else:
            start = None
        if params.has_key('to'):
            end = float(str(params['to']))
        else:
            end = None
        
        sql = '''
        select model.model_id, model_name, element_name, element_order, bp.pos, element.s, 
        alpha_x, alpha_y, beta_x, beta_y, eta_x, eta_y, etap_x, etap_y, nu_x, nu_y
        from model
        left join lattice on lattice.lattice_id = model.lattice_id
        left join element on element.lattice_id = lattice.lattice_id
        left join beam_parameter bp on bp.element_id = element.element_id and bp.model_id = model.model_id
        where model_name
        '''
        sqlvals = []
        if "*" in name or "%" in name:
            name = _wildcardformat(name)
            sql += " like %s "
        else:
            sql += " = %s "
        sqlvals.append(name)
        if start != None and end != None:
            sql += ' and element.s between %s and %s '
            sqlvals.append(start)
            sqlvals.append(end)
        elif start != None:
            sql += ' and element.s >= %s '
            sqlvals.append(start)
        elif end != None:
            sql += ' and element.s <= %s '
            sqlvals.append(end)

        try:
            sql += " order by bp.pos "
            cur=self.conn.cursor()
            cur.execute(sql, sqlvals)
            results = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving closed orbit:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving closed orbit:\n%s (%d)'
                             %(e.args[1], e.args[0]))
        resdict = OrderedDict()
        if len(results) != 0:
            modelid = results[0][0]
            modelname = results[0][1]
            ename = []
            order = []
            pos = []
            alphax = []
            alphay = []
            betax = []
            betay = []
            etax = []
            etay = []
            etapx = []
            etapy = []
            nux=[]
            nuy=[]
            for res in results:
                if modelid == res[0] and modelname == res[1]:
                    ename.append(res[2])
                    order.append(res[3])
                    pos.append(res[4])
                    alphax.append(res[6])
                    alphay.append(res[7])
                    betax.append(res[8])
                    betay.append(res[9])
                    etax.append(res[10])
                    etay.append(res[11])
                    etapx.append(res[12])
                    etapy.append(res[13])
                    nux.append(res[14])
                    nuy.append(res[15])
                else:
                    # when retrieving 
                    resdict[modelname] = {'name': ename,
                                          'index': order,
                                          'position': pos,
                                          'alphax': alphax,
                                          'alphay': alphay,
                                          'betax':  betax,
                                          'betay':  betay,
                                          'etax':   etax,
                                          'etay':   etay,
                                          'etapx':  etapx,
                                          'etapy':  etapy,
                                          'phasex': nux,
                                          'phasey': nuy}
                    modelid = results[0][0]
                    modelname = results[0][1]
                    alphax = []
                    alphay = []
                    betax = []
                    betay = []
                    etax = []
                    etay = []
                    etapx = []
                    etapy = []
                    nux=[]
                    nuy=[]
                # save last value
                resdict[modelname] = {'name': ename,
                                      'index': order,
                                      'position': pos,
                                      'alphax': alphax,
                                      'alphay': alphay,
                                      'betax':  betax,
                                      'betay':  betay,
                                      'etax':   etax,
                                      'etay':   etay,
                                      'etapx':  etapx,
                                      'etapy':  etapy,
                                      'phasex': nux,
                                      'phasey': nuy}

        return resdict
    
    def retrievebeamparameters(self, params):
        '''
        Retrieve all beam parameters of each element that satisfies given constrains.
        parameters:
            modelname:   the name shows that which model this API will deal with
            from:        index of starting element
            to:          index of ending element
        
        return: a dictionary
                {'model name':  # model name
                    {
                        'name': [element name],
                        'index': [element index],
                        'position': [s position],
                        'alphax': [],
                        'alphay': [],
                        'betax':  [],
                        'betax':  [],
                        'etax':   [],
                        'etay':   [],
                        'etapx':  [],
                        'etapy':  [],
                        'phasex': [],
                        'phasey': [],
                        'codx',   [],
                        'cody',   [],
                        'transferMatrix':[[transfer matrix],],
                    }
                 ...
                }
        '''
        if params.has_key('modelname'):
            name=params['modelname']
        else:
            raise TypeError('Not model name specified.')
        if params.has_key('from'):
            start = float(str(params['from']))
        else:
            start = None
        if params.has_key('to'):
            end = float(str(params['to']))
        else:
            end = None
        
        sql = '''
        select model.model_id, model_name, element_name, element_order, bp.pos, element.s, 
        alpha_x, alpha_y, beta_x, beta_y, eta_x, eta_y, etap_x, etap_y, nu_x, nu_y,
        co_x, co_y, 
        transfer_matrix
        from model
        left join lattice on lattice.lattice_id = model.lattice_id
        left join element on element.lattice_id = lattice.lattice_id
        left join beam_parameter bp on bp.element_id = element.element_id and model.model_id = bp.model_id
        where model_name
        '''
        sqlvals = []
        if "*" in name or "%" in name:
            name = _wildcardformat(name)
            sql += " like %s "
        else:
            sql += " = %s "
        sqlvals.append(name)
        if start != None and end != None:
            sql += ' and element.s between %s and %s '
            sqlvals.append(start)
            sqlvals.append(end)
        elif start != None:
            sql += ' and element.s >= %s '
            sqlvals.append(start)
        elif end != None:
            sql += ' and element.s <= %s '
            sqlvals.append(end)
            
        

        try:
            sql += " order by bp.pos "
            cur=self.conn.cursor()
            cur.execute(sql, sqlvals)
            results = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving closed orbit:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving closed orbit:\n%s (%d)'
                             %(e.args[1], e.args[0]))
        
        resdict = OrderedDict()
        if len(results) != 0:
            modelid = results[0][0]
            modelname = results[0][1]
            ename = []
            order = []
            pos = []
            alphax = []
            alphay = []
            betax = []
            betay = []
            etax = []
            etay = []
            etapx = []
            etapy = []
            nux=[]
            nuy=[]
            codx=[]
            cody=[]
            tmat = []
            for res in results:
                if modelid == res[0] and modelname == res[1]:
                    ename.append(res[2])
                    order.append(res[3])
                    pos.append(res[4])
                    alphax.append(res[6])
                    alphay.append(res[7])
                    betax.append(res[8])
                    betay.append(res[9])
                    etax.append(res[10])
                    etay.append(res[11])
                    etapx.append(res[12])
                    etapy.append(res[13])
                    nux.append(res[14])
                    nuy.append(res[15])
                    codx.append(res[16])
                    cody.append(res[17])
                    tmat.append(json.loads(res[18]))
                else:
                    # when retrieving 
                    resdict[modelname] = {'name': ename,
                                          'index': order,
                                          'position': pos,
                                          'alphax': alphax,
                                          'alphay': alphay,
                                          'betax':  betax,
                                          'betay':  betay,
                                          'etax':   etax,
                                          'etay':   etay,
                                          'etapx':  etapx,
                                          'etapy':  etapy,
                                          'phasex': nux,
                                          'phasey': nuy,
                                          'codx': codx,
                                          'cody': cody,
                                          'transferMatrix': tmat}
                    modelid = results[0][0]
                    modelname = results[0][1]
                    alphax = []
                    alphay = []
                    betax = []
                    betay = []
                    etax = []
                    etay = []
                    etapx = []
                    etapy = []
                    nux=[]
                    nuy=[]
                    codx=[]
                    cody=[]
                    tmat = []
                # save last value
                resdict[modelname] = {'name': ename,
                                      'index': order,
                                      'position': pos,
                                      'alphax': alphax,
                                      'alphay': alphay,
                                      'betax':  betax,
                                      'betay':  betay,
                                      'etax':   etax,
                                      'etay':   etay,
                                      'etapx':  etapx,
                                      'etapy':  etapy,
                                      'phasex': nux,
                                      'phasey': nuy,
                                      'codx': codx,
                                      'cody': cody,
                                      'transferMatrix': tmat}

        return resdict
#    def retrieveemittance(self):
#        '''
#        '''
#
#    def retrievebeamcoordinate(self):
#        '''
#        '''
    
    
    
    
