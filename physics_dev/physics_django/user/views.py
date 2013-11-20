from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout

try:
    from django.utils import simplejson as json
except ImportError:
    import json

@require_http_methods(["GET", "POST"])
def user_login(request):
    '''
    Authenticate user if credetials match
    '''
    result = {'result': ''}
    
    print request.POST
    
    username = request.POST.getlist('username')[0]
    password = request.POST.getlist('password')[0]
    print username, password
    user = authenticate(username=username, password=password)
    
    # Check if we got user object
    if user is not None:
        
        # If user is active, log him in
        if user.is_active:
            login(request, user)
            result['result'] = 'ok'
            
        # User exists but is not active
        else:
            result['result'] = 'error'
            
    # User doesnt exist in the database
    else:
        result['result'] = 'error'
    
    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["GET", "POST"])
def user_logout(request):
    '''
    Log user out
    '''
    result = {'result': 'ok'}
    logout(request)
    
    return HttpResponse(json.dumps(result), mimetype="application/json")