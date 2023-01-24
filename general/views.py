import datetime
import json
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from general.decorators import check_mode
from general.forms import OccassionForm, SubOccassionForm, CouponForm, PersonTypeForm, DueDaysForm, PhoneForm, \
    GiftImageForm, ExtrasForm, SliderForm
from general.functions import get_auto_id, generate_form_errors
from general.models import Occassion, SubOccassion, SetCoupon, PersonType, SetDueDays, Phone, GiftImage, Extras, Slider


class OccassionAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Occassion.objects.none()

        items = Occassion.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(occassion__icontains=query))

        return items


class SubOccassionAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return SubOccassion.objects.none()

        items = SubOccassion.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(sub_occassion__icontains=query))

        return items


class PersonTypeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PersonType.objects.none()

        items = PersonType.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(person_type__icontains=query))

        return items


@check_mode
@login_required
def app(request):
    return HttpResponseRedirect(reverse('dashboard'))


@check_mode
@login_required
def dashboard(request):
    context = {
        "title": "Dashboard",

        "is_dashboard": True,

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
    return render(request, "base.html", context)


@login_required
def create_occassion(request):
    if request.method == "POST":
        form = OccassionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Occassion)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title':'Successfully Created',
                'message': 'Occassion Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:occassion', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = OccassionForm()
        context = {
            "form": form,
            "title": "Create Occassion",
            "redirect": True,
            "url": reverse("general:create_occassion"),
            "is_occassion": True,
            "is_general": True,

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

        return render(request, 'general/occassion/entry.html', context)


@login_required
def occassion(request, pk):
    instance = get_object_or_404(Occassion.objects.filter(pk=pk))
    context = {
        "title": "Occassion : " + instance.occassion,
        "instance": instance,
        "is_occassion": True,
        "is_general": True,

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

    return render(request, 'general/occassion/occassion.html', context)


@login_required
def occassions(request):
    instances = Occassion.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(occassion__icontains=query))
    context = {
        "title": "Occassions",
        "instances": instances,
        "is_occassion": True,
        "is_general": True,

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

    return render(request, 'general/occassion/occassions.html', context)


@login_required
def edit_occassion(request, pk):
    instance = get_object_or_404(Occassion.objects.filter(pk=pk))
    if request.method == "POST":
        form = OccassionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title':'Successfully Updated',
                'message': 'Occassion Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:occassion', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = OccassionForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Occassion",
            "redirect": True,
            "url": reverse("general:edit_occassion", kwargs={"pk": pk}),
            "pk": pk,
            "is_occassion": True,
            "is_general": True,
            "instance":instance,

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

        return render(request, 'general/occassion/entry.html', context)


@login_required
def delete_occassion(request, pk):
    Occassion.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Occassion Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:occassions')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_sub_occassion(request):
    if request.method == "POST":
        form = SubOccassionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(SubOccassion)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Suboccassion Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:sub_occassion', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = SubOccassionForm()
        context = {
            "form": form,
            "title": "Create Sub Occassion",
            "redirect": True,
            "url": reverse("general:create_sub_occassion"),
            "is_sub_occassion": True,
            "is_general": True,

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

        return render(request, 'general/sub_occassion/entry.html', context)


@login_required
def sub_occassions(request):
    instances = SubOccassion.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(sub_occassion__icontains=query))
    context = {
        "title": "Sub Occassions",
        "instances": instances,
        "is_sub_occassion": True,
        "is_general": True,

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

    return render(request, 'general/sub_occassion/sub_occassions.html', context)


@login_required
def sub_occassion(request, pk):
    instance = get_object_or_404(SubOccassion.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.sub_occassion,
        "instance": instance,
        "is_sub_occassion": True,
        "is_general": True,

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

    return render(request, 'general/sub_occassion/sub_occassion.html', context)


@login_required
def edit_sub_occassion(request, pk):
    instance = get_object_or_404(SubOccassion.objects.filter(pk=pk))
    if request.method == "POST":
        form = SubOccassionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Suboccassion Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:sub_occassion', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = SubOccassionForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Suboccassion",
            "redirect": True,
            "url": reverse("general:edit_sub_occassion", kwargs={"pk": pk}),
            "pk": pk,
            "is_category": True,
            "is_product": True,
            "instance":instance,

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

        return render(request, 'general/sub_occassion/entry.html', context)


@login_required
def delete_sub_occassion(request, pk):
    SubOccassion.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Sub Occassion Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:sub_occassions')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(SetCoupon)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Coupon Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:coupon', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = CouponForm()
        context = {
            "form": form,
            "title": "Create Coupon",
            "redirect": True,
            "url": reverse("general:create_coupon"),
            "is_coupon": True,

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

        return render(request, 'general/coupon/entry.html', context)


@login_required
def coupon(request, pk):
    instance = get_object_or_404(SetCoupon.objects.filter(pk=pk))
    context = {
        "title": "Coupon : " + instance.coupon_code,
        "instance": instance,
        "is_coupon": True,

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

    return render(request, 'general/coupon/coupon.html', context)


@login_required
def edit_coupon(request, pk):
    instance = get_object_or_404(SetCoupon.objects.filter(pk=pk))
    if request.method == "POST":
        form = CouponForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Coupon Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:coupon', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = CouponForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Coupon",
            "redirect": True,
            "url": reverse("general:edit_coupon", kwargs={"pk": pk}),
            "pk": pk,
            "is_coupon": True,

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

        return render(request, 'general/coupon/entry.html', context)


@login_required
def coupons(request):
    instances = SetCoupon.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(coupon_code__icontains=query))
    context = {
        "title": "Coupons",
        "instances": instances,
        "is_coupon": True,

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

    return render(request, 'general/coupon/coupons.html', context)


@login_required
def delete_coupon(request, pk):
    SetCoupon.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Coupon Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:coupons')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_person_type(request):
    if request.method == "POST":
        form = PersonTypeForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(PersonType)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Person Type Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:person_type', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = PersonTypeForm()
        context = {
            "form": form,
            "title": "Create Person Type",
            "redirect": True,
            "url": reverse("general:create_person_type"),
            "is_pt": True,

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

        return render(request, 'general/pt/entry.html', context)


@login_required
def person_type(request, pk):
    instance = get_object_or_404(PersonType.objects.filter(pk=pk))
    context = {
        "title": "Person Type : " + instance.person_type,
        "instance": instance,
        "is_pt": True,

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

    return render(request, 'general/pt/pt.html', context)


@login_required
def person_types(request):
    instances = PersonType.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(person_type__icontains=query))
    context = {
        "title": "Person Types",
        "instances": instances,
        "is_pt": True,

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

    return render(request, 'general/pt/pts.html', context)


@login_required
def delete_person_type(request, pk):
    PersonType.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Person Type Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:person_types')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_person_type(request, pk):
    instance = get_object_or_404(PersonType.objects.filter(pk=pk))
    if request.method == "POST":
        form = PersonTypeForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Person Type Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:person_type', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = PersonTypeForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Person Type",
            "redirect": True,
            "url": reverse("general:edit_person_type", kwargs={"pk": pk}),
            "pk": pk,
            "is_pt": True,

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

        return render(request, 'general/pt/entry.html', context)


@login_required
def create_due_day(request):
    if request.method == "POST":
        form = DueDaysForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(SetDueDays)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Due Days Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:due_day', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = DueDaysForm()
        context = {
            "form": form,
            "title": "Create Due Days",
            "redirect": True,
            "url": reverse("general:create_due_day"),
            "is_dd": True,

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

        return render(request, 'general/dd/entry.html', context)


@login_required
def edit_due_day(request, pk):
    instance = get_object_or_404(SetDueDays.objects.filter(pk=pk))
    if request.method == "POST":
        form = DueDaysForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Due Days Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:due_day', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = DueDaysForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Due Day",
            "redirect": True,
            "url": reverse("general:edit_due_day", kwargs={"pk": pk}),
            "pk": pk,
            "is_dd": True,

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

        return render(request, 'general/dd/entry.html', context)


@login_required
def due_day(request, pk):
    instance = get_object_or_404(SetDueDays.objects.filter(pk=pk))
    context = {
        "title": "Due Days : " + str(instance.no_of_days),
        "instance": instance,
        "is_dd": True,

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

    return render(request, 'general/dd/dd.html', context)


@login_required
def due_days(request):
    instances = SetDueDays.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(no_of_days__icontains=query))
    context = {
        "title": "Due Days",
        "instances": instances,
        "is_dd": True,

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

    return render(request, 'general/dd/dds.html', context)


@login_required
def delete_due_day(request, pk):
    SetDueDays.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Due Days Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:due_days')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_phone(request):
    if request.method == "POST":
        form = PhoneForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Phone)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Phone Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:occassion', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = PhoneForm()
        context = {
            "form": form,
            "title": "Create Phone",
            "redirect": True,
            "url": reverse("general:create_phone"),
            "is_occassion": True,
            "is_general": True,

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

        return render(request, 'general/phone/entry.html', context)


@login_required
def phones(request):
    instances = Phone.objects.all()
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(no_of_days__icontains=query))
    context = {
        "title": "Chat with Dett",
        "instances": instances,
        "is_phone": True,

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

    return render(request, 'general/phone/phones.html', context)


@login_required
def edit_phone(request, pk):
    instance = get_object_or_404(Phone.objects.filter(pk=pk))
    if request.method == "POST":
        form = PhoneForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Phone Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:phones')
            })

        else:
            return JsonResponse({'error': True, 'errors': form.errors, })

    else:
        form = PhoneForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Phone",
            "redirect": True,
            "url": reverse("general:edit_phone", kwargs={"pk": pk}),
            "pk": pk,
            "is_phone": True,

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

        return render(request, 'general/phone/entry.html', context)


@login_required
def create_image(request):
    if request.method == "POST":
        form = GiftImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(GiftImage)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': "Your Moments Sucessfully Created",
                "redirect": 'true',
                "redirect_url": reverse('general:images')
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = GiftImageForm()
        context = {
            "form": form,
            "title": "Create Your Moments",
            "redirect": True,
            "url": reverse("general:create_image"),
            "is_app": True,
            "is_create_image": True,

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

        return render(request, 'general/image/entry.html', context)


@login_required
def images(request):
    instances = GiftImage.objects.filter(is_deleted=False)
    query = request.GET.get('q')

    context = {
        "title": "Your Moments",
        "instances": instances,
        "is_app": True,
        "is_images": True,

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

    return render(request, 'general/image/images.html', context)


@login_required
def edit_image(request, pk):
    instance = get_object_or_404(GiftImage.objects.filter(pk=pk))
    if request.method == "POST":
        form = GiftImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title':'Successfully Updated',
                'message': 'Your Moments Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('general:images')
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = GiftImageForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Your Moments",
            "redirect": True,
            "url": reverse("general:edit_image", kwargs={"pk": pk}),
            "pk": pk,
            "is_app": True,
            "instance":instance,

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

        return render(request, 'general/image/entry.html', context)


@login_required
def delete_image(request, pk):
    GiftImage.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Your Moments Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:images')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def extras(request):
    instances = ProductCategory.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(category_name__icontains=query))
    context = {
        "title": "Other Charges",
        "instances": instances,
        "is_category": True,
        "is_product": True,

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

    return render(request, 'products/category/categories.html', context)


@login_required
def extras(request, pk):
    instance = get_object_or_404(Extras.objects.filter(pk=pk))
    if request.method == "POST":
        form = ExtrasForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Other Charges Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('general:extras', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form.errors, })

    else:
        form = ExtrasForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Charges",
            "redirect": True,
            "url": reverse("general:extras", kwargs={"pk": pk}),
            "pk": pk,
            "is_extra": True,
            "is_active_extra": True,

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

        return render(request, 'general/extras/entry.html', context)


@login_required
def create_slider(request):
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Slider)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'App Banner Created Sucessfully',
                "redirect": 'true',
                "redirect_url": reverse('general:slider',kwargs={"pk": data.pk}),
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = SliderForm()
        context = {
            "form": form,
            "title": "Create App Banner",
            "redirect": True,
            "url": reverse("general:create_slider"),
            "is_banner": True,
            "is_banners": True,

            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_animations": True,
        }

        return render(request, 'general/slider/entry.html', context)


@login_required
def sliders(request):
    instances = Slider.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(title__icontains=query))
    context = {
        "title": "App Banners",
        "instances": instances,
        "is_banner": True,
        "is_banners": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_animations": True,
    }

    return render(request, 'general/slider/sliders.html', context)


@login_required
def delete_slider(request, pk):
    Slider.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "App Banner Deleted Successfully",
        "redirect": "true",
        "redirect_url": reverse('general:sliders')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_slider(request, pk):
    instance = get_object_or_404(Slider.objects.filter(pk=pk))
    current_image_url = str(instance.image.url)
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'App Banner Updated Sucessfully',
                "redirect": 'true',
                "redirect_url": reverse('general:sliders')
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = SliderForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit App Banner",
            "redirect": True,
            "url": reverse("general:edit_slider", kwargs={"pk": pk}),
            "pk": pk,
            "image_url":current_image_url,

            "is_banner": True,
            "is_banners": True,

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

        return render(request, 'general/slider/entry.html', context)


@login_required
def slider(request,pk):
    instances = Slider.objects.get(pk=pk)

    context = {
        "title": "App Banner :" + instances.title,
        "instance": instances,
        "is_banner": True,
        "is_banners": True,

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

    return render(request, 'general/slider/slider.html', context)



def handler500(request):

    context = {
        "error_page" : True,
        'title' : "Error 500",
        "body_class":"inner error",
        "short_description" : "We're sorry! The server encountered an internal error",
    }
    template = "web/errors/500.html"
    response = render(request,template,context)

    response.status_code = 500
    return response


def handler404(request):

    context = {
        "error_page" : True,
        'title' : "Error 404",
        "body_class":"inner error",
        "short_description" : "It seems we can't find what you're looking for",
    }
    template = "web/errors/404.html"
    response = render(request,template,context)

    response.status_code = 404
    return response


def handler403(request):

    context = {
        "error_page" : True,
        'title' : "Error 403",
        "body_class":"inner error",
        "short_description" : "You're not authorized to view this page.",
    }
    template = "web/errors/403.html"
    response = render(request,template,context)

    response.status_code = 404
    return response





