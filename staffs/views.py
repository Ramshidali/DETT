import datetime
import json
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from general.functions import get_auto_id, generate_form_errors
from staffs.forms import DesignationForm, StaffForm
from staffs.models import Designation, Staff


class DesignationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Designation.objects.none()

        items = Designation.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query))

        return items


@login_required
def designations(request):

    instances = Designation.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(name__icontains=query))
    context = {
        "title": "Designations",
        "instances": instances,
        "is_des": True,
        "is_staff": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'staff/des/dess.html', context)


@login_required
def create_designation(request):
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Designation)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Designation Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('staffs:designation', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = DesignationForm()
        context = {
            "form": form,
            "title": "Create Designation",
            "redirect": True,
            "url": reverse("staffs:create_designation"),
            "is_des": True,
            "is_staff": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'staff/des/entry.html', context)


@login_required
def edit_designation(request, pk):
    instance = get_object_or_404(Designation.objects.filter(pk=pk))
    if request.method == "POST":
        form = DesignationForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Designation Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('staffs:designation', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = DesignationForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Designation",
            "redirect": True,
            "url": reverse("staffs:edit_designation", kwargs={"pk": pk}),
            "pk": pk,
            "is_des": True,
            "is_staff": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'staff/des/entry.html', context)


@login_required
def designation(request, pk):
    instance = get_object_or_404(Designation.objects.filter(pk=pk))
    context = {
        "title": "Designation : " + instance.name,
        "instance": instance,
        "is_des": True,
        "is_staff": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'staff/des/des.html', context)


@login_required
def delete_designation(request, pk):
    Designation.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Designation Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('staffs:designations')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.user = request.user
            data.auto_id = get_auto_id(Staff)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Staff Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('staffs:staff', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = StaffForm()
        context = {
            "form": form,
            "title": "Create Staff",
            "redirect": True,
            "url": reverse("staffs:create_staff"),
            "is_sf": True,
            "is_staff": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'staff/staff/entry.html', context)


@login_required
def edit_staff(request, pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk))
    if request.method == "POST":
        form = StaffForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Staff Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('staffs:staff', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = StaffForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Staff",
            "redirect": True,
            "url": reverse("staffs:edit_staff", kwargs={"pk": pk}),
            "pk": pk,
            "is_sf": True,
            "is_staff": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'staff/staff/entry.html', context)


@login_required
def staff(request, pk):
    instance = get_object_or_404(Staff.objects.filter(pk=pk))
    context = {
        "title": "Staff : " + instance.name,
        "instance": instance,
        "is_sf": True,
        "is_staff": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'staff/staff/staff.html', context)


@login_required
def staffs(request):
    instances = Staff.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(name__icontains=query))
    context = {
        "title": "Staffs",
        "instances": instances,
        "is_sf": True,
        "is_staff": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'staff/staff/staffs.html', context)


@login_required
def delete_staff(request, pk):
    Staff.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Staff Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('staffs:staffs')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
