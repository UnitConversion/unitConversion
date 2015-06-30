""" 
Created on Mar 10st, 2014
@author dejan.dezman@cosylab.com
"""

from django.conf.urls import patterns, url

from activeinterlock.views import (retrieveStatusesWS) 
from activeinterlock.views import (retrieveAiHeaderWS, saveAiHeaderWS, updateAiHeaderWS) 
from activeinterlock.views import (retrieveDeviceWS, saveDeviceWS, updateDeviceWS, deleteDeviceWS) 
from activeinterlock.views import (updateStatusWS, copyAiWS) 
from activeinterlock.views import (updatePropWS) 
from activeinterlock.views import (approveCellsWS) 
from activeinterlock.views import (retrieveLogicWS, saveLogicWS, updateLogicWS, deleteLogicWS) 
from activeinterlock.views import (downloadActiveInterlockWS) 
from activeinterlock.views import (aiIndexHtml, aiHtmls) 

urlpatterns = patterns(
    '',

    url(r'^ai/statuses/$', retrieveStatusesWS),

    url(r'^ai/activeinterlockheader/$', retrieveAiHeaderWS),
    url(r'^ai/saveactiveinterlockheader/$', saveAiHeaderWS),
    url(r'^ai/updateactiveinterlockheader/$', updateAiHeaderWS),

    url(r'^ai/device/$', retrieveDeviceWS),
    url(r'^ai/savedevice/$', saveDeviceWS),
    url(r'^ai/updatedevice/$', updateDeviceWS),
    url(r'^ai/deletedevice/$', deleteDeviceWS),
    
    url(r'^ai/updatestatus/$', updateStatusWS),
    url(r'^ai/copyactiveinterlock/$', copyAiWS),
    
    url(r'^ai/updateprop/$', updatePropWS),
    
    url(r'^ai/approve/$', approveCellsWS),
    
    url(r'^ai/logic/$', retrieveLogicWS),
    url(r'^ai/savelogic/$', saveLogicWS),
    url(r'^ai/updatelogic/$', updateLogicWS),
    url(r'^ai/deletelogic/$', deleteLogicWS),
    
    
    url(r'^ai/download/$', downloadActiveInterlockWS),

    url(r'^ai/web/$', aiIndexHtml),
    url(r'^ai/web/(.+)', aiHtmls),
)
