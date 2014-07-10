from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
import ldap
import traceback
import sys

try:
    from django.utils import simplejson as json
except ImportError:
    import json


@require_http_methods(["GET", "POST"])
def user_login(request):
    '''
    Authenticate user if credetials match
    '''

    try:
        result = {'result': ''}

        username = request.POST.getlist('username')[0]
        password = request.POST.getlist('password')[0]

        user = authenticate(username=username, password=password)

        # Check if we got user object
        if user is not None:

            # If user is active, log him in
            if user.is_active:
                login(request, user)
                result['result'] = 'ok'
                return HttpResponse(json.dumps(result), mimetype="application/json")

            # User exists but is not active
            else:
                return HttpResponse('Unauthorized', status=401)

        # User doesnt exist in the database
        else:
            return HttpResponse('Unauthorized', status=401)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e


@require_http_methods(["GET", "POST"])
def user_logout(request):
    '''
    Log user out
    '''
    result = {'result': 'ok'}
    logout(request)

    return HttpResponse(json.dumps(result), mimetype="application/json")