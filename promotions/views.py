import datetime
import json
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from promotions.models import Enquiry
from products.models import ProductImage


@login_required
def enquiries(request):
    instances = Enquiry.objects.filter(is_deleted=False,status=False)

    context = {
        "title": "Enquiries",
        "instances": instances,
        "is_enquiry": True,

        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_grid_system": True,
        "is_need_animations": True,
    }

    return render(request, 'promotions/enquiry/enquiries.html', context)


@login_required
def enquiry(request, pk):
    instance = get_object_or_404(Enquiry.objects.filter(pk=pk))
    product_image = ProductImage.objects.filter(product_variant=instance.product).first()

    context = {
        "title": "Enquiry Id : " + instance.enquiry_id,
        "instance": instance,
        "is_enquiry": True,

        "product_image":product_image,

        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_grid_system": True,
        "is_need_animations": True,
    }

    return render(request, 'promotions/enquiry/enquiry.html', context)


@login_required
def mark_as_read(request, pk):
    Enquiry.objects.filter(pk=pk).update(status=True)

    response_data = {
        "status": "true",
        "title": "Successfully Updated",
        "message": "Status Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('promotions:enquiries')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def marked_enquiries(request):
    instances = Enquiry.objects.filter(is_deleted=False,status=True)

    context = {
        "title": "Marked Enquiries",
        "instances": instances,
        "is_enquiry": True,

        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_grid_system": True,
        "is_need_animations": True,
    }

    return render(request, 'promotions/enquiry/enquiries.html', context)