import json

from django.db.models import Q
from django.urls import reverse
from django.http.response import HttpResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse

from users.forms import *
from users.models import *
from general.functions import generate_form_errors
from general.decorators import check_mode, ajax_required, check_mode

from django.db.models import Sum, Q



@check_mode
@login_required
def dashboard(request):
    return HttpResponseRedirect(reverse('app'))


@check_mode
@login_required
@ajax_required
@require_GET
def check_notification(request):
    user = request.user
    count = Notification.objects.filter(user=user,is_read=False,is_active=True,shop=current_shop).count()
    return HttpResponse(json.dumps(count), content_type='application/javascript')


@check_mode
@login_required
def notifications(request):
    title = "Notifications"
    instances = Notification.objects.filter(user=request.user,is_deleted=False,is_active=True,shop=current_shop)

    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(subject__name__icontains=query) | Q(product__name__icontains=query))
        title = "Notifications - %s" %query

    context = {
        'title' : title,
        "instances" : instances,
        "is_need_select_picker": True,
        "is_need_popup_box" : True,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
    }
    return render(request,"users/notifications.html",context)


@check_mode
@login_required
def delete_notification(request,pk):
    Notification.objects.filter(pk=pk,user=request.user).update(is_deleted=True,is_read=True)

    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Notification Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('users:notifications')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@check_mode
@login_required
def delete_selected_notifications(request):
    pks = request.GET.get('pk')
    if pks:
        pks = pks[:-1]

        pks = pks.split(',')
        for pk in pks:
            Notification.objects.filter(pk=pk,user=request.user).update(is_deleted=True,is_read=True)

        response_data = {
            "status" : "true",
            "title" : "Successfully Deleted",
            "message" : "Selected Notification(s) Successfully Deleted.",
            "redirect" : "true",
            "redirect_url" : reverse('users:notifications')
        }
    else:
        response_data = {
            "status" : "false",
            "title" : "Nothing selected",
            "message" : "Please select some items first.",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@check_mode
@login_required
def read_selected_notifications(request):
    pks = request.GET.get('pk')
    if pks:
        pks = pks[:-1]

        pks = pks.split(',')
        for pk in pks:
            Notification.objects.filter(pk=pk,user=request.user).update(is_deleted=True,is_read=True)

        response_data = {
            "status" : "true",
            "title" : "Successfully marked as read",
            "message" : "Selected notification(s) successfully marked as read.",
            "redirect" : "true",
            "redirect_url" : reverse('users:notifications')
        }
    else:
        response_data = {
            "status" : "false",
            "title" : "Nothing selected",
            "message" : "Please select some items first.",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@check_mode
@login_required
def read_notification(request,pk):
    Notification.objects.filter(pk=pk,user=request.user).update(is_read=True)

    response_data = {
        "status" : "true",
        "title" : "Successfully marked as read",
        "message" : "Notification successfully marked as read.",
        "redirect" : "true",
        "redirect_url" : reverse('users:notifications')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@ajax_required
@require_GET
def set_user_timezone(request):
    timezone = request.GET.get('timezone')
    request.session["set_user_timezone"] = timezone
    response_data = {}
    response_data['status'] = 'true'
    response_data['title'] = "Success"
    response_data['message'] = 'user timezone set successfully.'
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@check_mode
@login_required
def change_password(request,pk):
    instance = get_object_or_404(User.objects.filter(pk=pk,is_active=True))
    if request.method == "POST":
        response_data = {}
        form = PasswordChangeForm(user=instance, data=request.POST)
        if form.is_valid():
            form.save()

            response_data = {
                'status' : 'true',
                'title' : "Successfully Changed",
                'redirect' : 'false',
                'message' : "Password Successfully Changed."
            }
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                'status' : 'false',
                'stable' : 'true',
                'title' : "Form validation error",
                "message" : message,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        title = "Change Password"
        change_password_form = PasswordChangeForm(user=instance)
        context = {
            "change_password_form" : change_password_form,
            "title" : title,
            "instance" : instance,

            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_animations": True,
            "is_need_grid_system": True,
            "is_need_select_picker": True,
            "is_need_datetime_picker" : True
        }
        return render(request, 'users/change_password.html', context)

