from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from customers.models import Customer
from django.db.models import Sum, Q
from customers.models import MomentCard


@login_required
def customers(request):
    instances = Customer.objects.all()
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(name__icontains=query))
    context = {
        "title": "Customers",
        "instances": instances,
        "is_users": True,

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

    return render(request, 'customers/customer/customers.html', context)


def pdf(request):
    return render(request, 'pdf/invoice.html')


@login_required
def upcoming_moments(request):
    """
    function for getting the upcoming moments added by the different users
    :param request:
    """
    context = {}
    try:
        query = request.GET.get('q')

        is_current_month = False
        is_next_month = False

        # get all the events based on event date
        event_instances = MomentCard.objects.filter(is_deleted=False).order_by('event_date')
        current_month = datetime.now().month
        next_month = current_month + 1
        if query:
            if '1' in query:
                print("Current ")
                is_current_month = True
                event_instances = event_instances.filter(event_date__month=current_month).order_by('event_date')

            elif '2' in query:
                is_next_month = True
                event_instances = event_instances.filter(event_date__month=next_month).order_by('event_date')

    except Exception as e:
        context = {
            "error": True,
            "message": str(e)
        }

    else:
        context = {
            "title": "Upcoming Events",
            "instances": event_instances,
            "is_current_month":is_current_month,
            "is_next_month": is_next_month,
        }

    finally:
        return render(request, 'customers/events/events.html', context)
