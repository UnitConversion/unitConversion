""" 
Created on Mar 10st, 2014
@author dejan.dezman@cosylab.com
"""

from django.conf.urls.defaults import patterns, url

from physics_django.activeinterlock.views import (retrieveStatusesWS) 
from physics_django.activeinterlock.views import (retrieveAiHeaderWS, saveAiHeaderWS) 
from physics_django.activeinterlock.views import (retrieveDeviceWS, saveDeviceWS, updateDeviceWS) 
from physics_django.activeinterlock.views import (updateStatusWS) 
from physics_django.activeinterlock.views import (updatePropWS) 
from physics_django.activeinterlock.views import (approveCellsWS) 
from physics_django.activeinterlock.views import (retrieveLogicWS, saveLogicWS, updateLogicWS) 
from physics_django.activeinterlock.views import (downloadActiveInterlockWS) 
from physics_django.activeinterlock.views import (aiIndexHtml, aiHtmls) 

urlpatterns = patterns(
    '',

    url(r'^ai/statuses/$', retrieveStatusesWS),

    url(r'^ai/activeinterlockheader/$', retrieveAiHeaderWS),
    url(r'^ai/saveactiveinterlockheader/$', saveAiHeaderWS),

    url(r'^ai/device/$', retrieveDeviceWS),
    url(r'^ai/savedevice/$', saveDeviceWS),
    url(r'^ai/updatedevice/$', updateDeviceWS),
    
    url(r'^ai/updatestatus/$', updateStatusWS),
    
    url(r'^ai/updateprop/$', updatePropWS),
    
    url(r'^ai/approve/$', approveCellsWS),
    
    url(r'^ai/logic/$', retrieveLogicWS),
    url(r'^ai/savelogic/$', saveLogicWS),
    url(r'^ai/updatelogic/$', updateLogicWS),
    
    
    url(r'^ai/download/$', downloadActiveInterlockWS),

    url(r'^ai/web/$', aiIndexHtml),
    url(r'^ai/web/(.+)', aiHtmls),
)
