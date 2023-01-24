import json

from django.urls import reverse
from general.models import Mode
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse

from general.functions import get_current_role


def ajax_required(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return render(request,'error/400.html',{})
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


def check_mode(function):
    def wrap(request, *args, **kwargs):
        mode = Mode.objects.get(id=1)
        readonly = mode.readonly
        maintenance = mode.maintenance
        down = mode.down

        if down:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application currently down. Please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('down'))
        elif readonly:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application now readonly mode. please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('read_only'))

        return function(request, *args, **kwargs)

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


def role_required(roles):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            current_role = get_current_role(request)
            if not current_role in roles:
                if request.is_ajax():
                    response_data = {
                        "status": "false",
                        "stable": "true",
                        "title": "Permission Denied",
                        "message": "You have no permission to do this action."
                    }
                    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                else:
                    context = {
                        "title" : "Permission Denied"
                    }
                    return render(request, 'error/permission_denied.html', context)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper