from django.shortcuts import render, get_object_or_404
from orders.models import Order, OrderItem, OrderStatus
from orders.forms import OrderChargesForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
import datetime
from django.db.models import Q
from general.utils.sms import SMS


@login_required
def orders(request):
    instances = Order.objects.filter(is_deleted=False, order_status__in=['10', '20', '30', '40']).order_by(
        '-date_added')
    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(billing_name__icontains=query))
    context = {"title": "Orders", "instances": instances, "is_order": True, "is_active_order": True,

        "is_need_select_picker": True, "is_need_popup_box": True, "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True, "is_need_bootstrap_growl": True, "is_need_chosen_select": True,
        "is_need_grid_system": True, "is_need_datetime_picker": True, "is_need_animations": True, }

    return render(request, 'orders/orders.html', context)


@login_required
def cancelled_orders(request):
    instances = Order.objects.filter(is_deleted=False, order_status='0').order_by('-date_added')
    query = request.GET.get('q')

    if query:
        instances = instances.filter(Q(billing_name__icontains=query))
    context = {"title": "Orders", "instances": instances, "is_order": True, "is_cancelled_order": True,

        "is_need_select_picker": True, "is_need_popup_box": True, "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True, "is_need_bootstrap_growl": True, "is_need_chosen_select": True,
        "is_need_grid_system": True, "is_need_datetime_picker": True, "is_need_animations": True, }

    return render(request, 'orders/orders.html', context)


@login_required
def completed_orders(request):
    instances = Order.objects.filter(is_deleted=False, order_status='50').order_by('-date_added')
    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(billing_name__icontains=query))
    context = {"title": "Orders", "instances": instances, "is_order": True, "is_completed_order": True,

        "is_need_select_picker": True, "is_need_popup_box": True, "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True, "is_need_bootstrap_growl": True, "is_need_chosen_select": True,
        "is_need_grid_system": True, "is_need_datetime_picker": True, "is_need_animations": True, }

    return render(request, 'orders/orders.html', context)


@login_required
def order(request, pk):
    instance = get_object_or_404(Order.objects.filter(pk=pk))
    order_items = OrderItem.objects.filter(order=instance)
    order_status = OrderStatus.objects.filter(order=pk)

    if request.method == "POST":
        sms_manager = SMS(instance.billing_phone)
        order_status = instance.order_status
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        if order_status == '10':

            instance.order_status = 20
            instance.date_updated = datetime.date.today()
            instance.save()
            OrderStatus.objects.create(status='20', order=instance, )
            # sms_manager.gift_booked(instance.invoice_id)
            sms_manager.gift_packed(instance.invoice_id)

        elif order_status == '20':
            instance.order_status = 30
            instance.date_updated = datetime.date.today()
            instance.save()
            OrderStatus.objects.create(status='30', order=instance,
            )
            # sms_manager.gift_packed(instance.invoice_id)
            sms_manager.gift_shipped(instance.invoice_id)
            
        elif order_status == '30':
            instance.order_status = 40
            instance.date_updated = datetime.date.today()
            instance.save()
            OrderStatus.objects.create(status='40', order=instance,
            )
            # sms_manager.gift_shipped(instance.invoice_id)
            sms_manager.gift_out_for_delivery(instance.invoice_id)

        elif order_status == '40':
            instance.order_status = 50
            instance.date_updated = datetime.date.today()
            instance.save()
            OrderStatus.objects.create(status='50', order=instance,

            )
            # sms_manager.gift_out_for_delivery(instance.invoice_id)
            sms_manager.gift_delivered(instance.invoice_id)
            
        elif order_status == '50':
            instance.order_status = 50
            instance.date_updated = datetime.date.today()
            instance.save()
            OrderStatus.objects.create(status='50', order=instance,

            )
            # sms_manager.gift_delivered(instance.invoice_id)

        return JsonResponse({"status": "true", 'error': False, 'message': 'Order Status Updated', "redirect": 'true',
            "redirect_url": reverse('orders:order', kwargs={"pk": instance.pk})})

    context = {
        "title": "Order : " + instance.billing_name + ",  " + "Delivery Date ",
        "order_items": order_items, "instance": instance, "order_status": order_status,
        # + " :- " + instance.delivery_date.date,

        "is_order": True, "redirect": True, "url": reverse("orders:order", kwargs={"pk": pk}),

        "is_need_select_picker": True, "is_need_popup_box": True, "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True, "is_need_bootstrap_growl": True, "is_need_chosen_select": True,
        "is_need_grid_system": True, "is_need_datetime_picker": True, "is_need_animations": True, }

    return render(request, 'orders/order.html', context)


@login_required
def assign_charges(request, pk):
    instance = get_object_or_404(Order.objects.filter(pk=pk))
    if request.method == "POST":
        form = OrderChargesForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()

            return JsonResponse({"status": "true", 'error': False, 'message': 'Charges Updated', "redirect": 'true',
                "redirect_url": reverse('orders:order', kwargs={"pk": pk})})

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = OrderChargesForm(instance=instance)
        context = {
            "form": form, 
            "title": "Add Charges", 
            "redirect": True,
            "url": reverse("orders:assign_charges", kwargs={"pk": pk}),

            "is_need_select_picker": True, "is_need_popup_box": True, "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True, "is_need_bootstrap_growl": True, "is_need_chosen_select": True,
            "is_need_grid_system": True, "is_need_datetime_picker": True, "is_need_animations": True, 
        }

        return render(request, 'orders/entry.html', context)
