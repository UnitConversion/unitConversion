'''
The service side data process functions are implemented in this module.

'''

from django.db import connection, transaction
from _mysql_exceptions import MySQLError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pyactiveinterlock.epsai import epsai

from utils.utils import _checkkeys

epsaiinst = epsai(connection, transaction=transaction)

def retrieveactiveinterlock(params):
    '''Retrieve a data set according its saved time, and status.
    One data set should have same properties for all device although its value could be empty.

    This method calls ``epsai.retrieveactiveinterlock`` directly, therefore 
    all parameters have to fit requirement of ``epsai.retrieveactiveinterlock``.

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.retrieveactiveinterlock``.
    :type params: dict
    
    :returns: A Python dictionary is returned like as described in ``epsai.retrieveactiveinterlock``.

    :raises: ValueError
    '''
    
    status='*'
    if params.has_key('status'):
        status=params['status']
    datefrom=None
    if params.has_key('datefrom'):
        datefrom=params['datefrom']
    dateto=None
    if params.has_key('dateto'):
        dateto=params['dateto']
    withdata=True
    if params.has_key('withdata'):
        withdata=bool(json.loads(params['withdata'].lower()))
    rawdata=False
    if params.has_key('rawdata'):
        rawdata=bool(json.loads(params['rawdata'].lower()))

    return epsaiinst.retrieveactiveinterlock(status, datefrom=datefrom, dateto=dateto, withdata=withdata, rawdata=rawdata)
    
def saveactiveinterlock(params):
    '''Save a new data set of active interlock.
    By default, it deactivates existing active data set, and active this new data set.
    Only one active data is allowed.
    
    A logic of active interlock has to be saved first, otherwise, an AttributeError might raise if logic can not be found.

    This method calls ``epsai.saveactiveinterlock`` directly, therefore 
    all parameters have to fit requirement of ``epsai.saveactiveinterlock``.

    Different with ``epsai.saveactiveinterlock``, the ``data`` structure has to be serialized into a JSON string before shipping over network.
    

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.saveactiveinterlock``.
    :type params: dict
    
    :returns: A Python dictionary is returned as: ::
    
        {'id': ai_id}

    :raises: ValueError
    '''
    _checkkeys(params.keys(), ['function','data', 'description', 'rawdata', 'active', 'author'])

    if params.has_key('data'):
        data=json.loads(params['data'])
    else:
        raise ValueError('Cannot find data to save')

    description=None
    if params.has_key('description'):
        description=params['description']

    rawdata=None
    if params.has_key('rawdata'):
        rawdata=params['rawdata']

    active=True
    if params.has_key('active'):
        active=bool(json.loads(params['active'].lower()))
    
    author=None
    if params.has_key('author'):
        author=params['author']
        
    try:
        res = epsaiinst.saveactiveinterlock(data, 
                                            description=description, 
                                            rawdata=rawdata, 
                                            active=active, 
                                            author=author)
        transaction.commit_unless_managed()

    except MySQLError as e:
        transaction.rollback_unless_managed()
        epsaiinst.logger.info('Data set error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
        raise
    except KeyError as e:
        epsaiinst.logger.info('Data set error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
        raise e

    return {'id': res}

def updateactiveinterlockstatus(params):
    '''Update status of a data set.
    Once data is saved into database, only its status is allowed to be updated between active & inactive.
    Only up to one (1) data set is allowed to be active. When the status is to active a particular data set,
    it deactivates current active data set.
    
    This method calls ``epsai.updateactiveinterlockstatus`` directly, therefore 
    all parameters have to fit requirement of ``epsai.updateactiveinterlockstatus``.

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.updateactiveinterlockstatus``.
    :type params: dict
    
    :returns: A Python dictionary is returned as: ::
    
        {'result': True}

        when the result is "True", it means the status has been changed; or "False" when the status is not changed.

    :raises: ValueError

    '''
    _checkkeys(params.keys(), ['function','id', 'status', 'author'])

    aiid=None
    if params.has_key('id'):
        aiid = params['id']
    else:
        raise ValueError('Cannot find internal id of a data set to be updated.')

    status = None
    if params.has_key('status'):
        status = int(params['status'])
    else:
        raise ValueError('Cannot find status of a data set to be updated to.')
    author = None
    if params.has_key('author'):
        author = params['author']

    try:
        res = epsaiinst.updateactiveinterlockstatus(aiid, status=status, author=author)
        transaction.commit_unless_managed()
    except MySQLError as e:
        transaction.rollback_unless_managed()
        epsaiinst.logger.info('Error when updating active interlock data set (id: %s) status:\n%s (%d)' %(e.args[1], e.args[0], aiid))
        raise
    
    return {'status': res}

def retrieveactiveinterlockproptype(params):
    '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
    This method is to retrieve active interlock property type information with given name, unit, and/or description.
    
    Wildcast matching is supported with:
    
        - ``*`` for multiple characters match, 
        - ``?`` for single character match.

    This method calls ``epsai.retrieveactiveinterlockproptype`` directly, therefore 
    all parameters have to fit requirement of ``epsai.retrieveactiveinterlockproptype``.

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.retrieveactiveinterlockproptype``.
    :type params: dict
    
    :returns: A Python dictionary is returned like as described in ``epsai.retrieveactiveinterlockproptype``.

    :raises: ValueError
    
    '''
    
    _checkkeys(params.keys(), ['function','name', 'unit', 'description'])
    name = None
    if params.has_key('name'):
        name=params['name']
    else:
        raise ValueError('Property type name for an active interlock unit is not given')

    unit=None
    if params.has_key('unit'):
        unit=params['unit']
    description=None
    if params.has_key('description'):
        description=params['description']

    return epsaiinst.retrieveactiveinterlockproptype(name, unit=unit, description=description)

def saveactiveinterlockproptype(params):
    '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
    This method is to save active interlock property type information with given name, unit, and/or description.
    
    The property name with given unit is unique in the database. It allows user to reuse a property type name, but given it 
    a different unit.
    
    This method calls ``epsai.saveactiveinterlockproptype`` directly, therefore 
    all parameters have to fit requirement of ``epsai.saveactiveinterlockproptype``.

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.saveactiveinterlockproptype``.
    :type params: dict
    
    :returns: A Python dictionary is returned like: ::
    
        {'id': property_type_id}

    :raises: ValueError, MySQLError

    '''
    _checkkeys(params.keys(), ['function','name', 'unit', 'description'])
    name = None
    if params.has_key('name'):
        name=params['name']
    else:
        raise ValueError('Property type name for an active interlock unit is not given')
    
    unit=None
    if params.has_key('unit'):
        unit=params['unit']
    description=None
    if params.has_key('description'):
        description=params['description']
    try:
        res = epsaiinst.saveactiveinterlockproptype(name,
                                                    unit=unit,
                                                    description=description 
                                                    )
        
        transaction.commit_unless_managed()
    except MySQLError as e:
        transaction.rollback_unless_managed()
        epsaiinst.logger.info('Data set error when saving active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
        raise

    return {'id': res}
    
def retrieveactiveinterlocklogic(params):
    '''Retrieve logic information according given search constrains.
    Wildcast matching is supported for name and shape with:
    
        - ``*`` for multiple characters match, 
        - ``?`` for single character match.

    This method calls ``epsai.retrieveactiveinterlocklogic`` directly, therefore 
    all parameters have to fit requirement of ``epsai.retrieveactiveinterlocklogic``.

    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.retrieveactiveinterlocklogic``.
    :type params: dict
    
    :returns: A Python dictionary is returned like as described in ``epsai.retrieveactiveinterlocklogic``.
    
    :raises: ValueError
    '''
    _checkkeys(params.keys(), ['function','name', 'shape', 'logic'])
    name = None
    if params.has_key('name'):
        name=params['name']
    else:
        raise ValueError('Active interlock envelop name is not given')

    shape=None
    if params.has_key('shape'):
        shape=params['shape']
    
    logic=None
    if params.has_key('logic'):
        logic=params['logic']
    
    return epsaiinst.retrieveactiveinterlocklogic(name, shape=shape, logic=logic)

def saveactiveinterlocklogic(params):
    '''Save logic information for active interlock system.
    
    This method calls ``epsai.saveactiveinterlocklogic`` directly, therefore 
    all parameters have to fit requirement of ``epsai.saveactiveinterlocklogic``.
    
    :param params: dictionary for active interlock logic. Detailed params please see ``epsai.saveactiveinterlocklogic``.
    :type params: dict
    
    :returns: A Python dictionary is returned like: ::
    
        {'id': ai_logic_id}
    
    :raises: ValueError, MySQLError

    '''

    _checkkeys(params.keys(), ['function','name', 'shape', 'logic', 'logiccode', 'author'])
    name = None
    if params.has_key('name'):
        name=params['name']
    else:
        raise ValueError('Active interlock envelop name is not given')
    
    shape=None
    if params.has_key('shape'):
        shape=params['shape']
    else:
        raise ValueError('Shape for active interlock envelop (%s) is not given.'%name)
    
    logic=None
    if params.has_key('logic'):
        logic=params['logic']
    else:
        raise ValueError('Logic expression for active interlock envelop (%s) is not given.'%name)
    
    logiccode=None
    if params.has_key('logiccode'):
        logiccode=params['logiccode']
    else:
        raise ValueError('Logic code for active interlock envelop (%s) is not given.'%name)
        
    author=None
    if params.has_key('author'):
        author=params['author']

    try:
        res = epsaiinst.saveactiveinterlocklogic(name, 
                                                 shape, 
                                                 logic, 
                                                 logiccode, 
                                                 author=author)
        
        transaction.commit_unless_managed()
    except MySQLError as e:
        transaction.rollback_unless_managed()
        epsaiinst.logger.info('Data set error when saving active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
        raise

    return {'id': res}

