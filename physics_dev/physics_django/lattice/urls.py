from django.conf.urls.defaults import patterns, url

from physics_django.lattice.views import (lattices)
from physics_django.lattice.views import (saveLatticeInfo, saveLattice)
from physics_django.lattice.views import (lattice_home, lattice_content_home, lattice_content_search, lattice_content_list, lattice_content_model_list, lattice_content_details, lattice_content_model_details)
from physics_django.lattice.views import (lattice_modal, saveLatticeHelper, saveModelHelper, saveModelStatusHelper)

urlpatterns = patterns(
    '',
    # return raw data not thru html ui
    url(r'^lattice/$',
        lattices,
        name='lattices'),
    
    url(r'^lattice/savelatticeinfo/$',
        saveLatticeInfo,
        name='saveLatticeInfo'),
    
    url(r'^lattice/savelattice/$',
        saveLattice,
        name='saveLattice'),
#    url(r'^lattice/model/$',
#        models,
#        name='model'),
    url(r'^lattice/web/$',
        lattice_home,
        name='lattice_home'),
    url(r'^lattice/web/index.html$',
        lattice_home,
        name='lattice_home'),
    url(r'^lattice/web/content.html$',
        lattice_content_home,
        name='lattice_content_home'),
    url(r'^lattice/web/search.html$',
        lattice_content_search,
        name='lattice_content_search'),
    url(r'^lattice/web/list.html$',
        lattice_content_list,
        name='lattice_content_list'),
    url(r'^lattice/web/model_list.html$',
        lattice_content_model_list,
        name='lattice_content_model_list'),
    url(r'^lattice/web/details.html$',
        lattice_content_details,
        name='lattice_content_details'),
    url(r'^lattice/web/model_details.html$',
        lattice_content_model_details,
        name='lattice_content_model_details'),
    
    url(r'^lattice/web/modal/',
        lattice_modal,
        name='lattice_modal'),
    
    url(r'^lattice/upload$',
        saveLatticeHelper,
        name='saveLatticeHelper'),

    url(r'^model/upload$',
        saveModelHelper,
        name='saveModelHelper'),

    url(r'^model/savestatus$',
        saveModelStatusHelper,
        name='saveModelStatusHelper'),
)
