import datetime
from reports.functions import get_hsn_totals, get_sac_totals
from django.shortcuts import render
from orders.models import Order


def gstr1_report(request):
    """
    This is a report that is the total of all order and order_returns
    calculation is as follows
    1) get total of order items excluding tax from orders
    2) and deduct each taxable amount with given tax percentage
    :param request:
    :return:
    """
    context = {}

    try:
        # getting dates
        today = datetime.datetime.now().date()
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        data = {}

        get_hsn_total = get_hsn_totals(request)
        get_sac_total = get_sac_totals(request)

        # taking orders
        orders = Order.objects.filter(is_deleted=False).order_by(
            'date_added')
        instances = orders

        print("Dates...")
        print(from_date)
        print(to_date)
        # if request has date
        if from_date and to_date:
            data = {"from_date": from_date, "to_date": to_date, }
            # formatting date to dd/mm/yyyy format
            try:
                print(from_date)
                from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
                to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

                get_hsn_total = get_hsn_totals(request)
                get_sac_total = get_sac_totals(request)

                instances = Order.objects.filter(is_deleted=False,date_added__range=[from_date,to_date]).order_by(
                    'date_added')

            except Exception as e:
                date_error = "yes"
                print("error===>>>",e)

    except Exception as e:
        print(e)
        context = {"is_error": True, "error": str(e), }

    else:
        context = {"title": "GSTR1 Report", "instances": instances, "get_hsn_totals": get_hsn_total,
                   "get_sac_total": get_sac_total,"data": data ,"is_need_select_picker": True, "is_need_popup_box": True,
                   "is_need_custom_scroll_bar": True, "is_need_wave_effect": True, "is_need_bootstrap_growl": True,
                   "is_need_chosen_select": True, "is_need_grid_system": True, "is_need_datetime_picker": True,
                   "is_need_animations": True, }

    return render(request, 'reports/gstr1/report.html', context)
