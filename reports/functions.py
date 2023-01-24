import sys
from orders.models import Order, OrderItem
from django.db.models import Sum
import decimal
import datetime


def get_hsn_totals(request):
    """
    get all the hsn total fields
    """
    response_data = {}
    try:

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # order items total price
        total_without_tax = OrderItem.objects.aggregate(Sum('price'))['price__sum'] or 0

        # order items
        order_items = OrderItem.objects.filter(is_deleted=False)

        # if dates
        if from_date and to_date:
            from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
            to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

            total_without_tax = OrderItem.objects.filter(date_added__range=[from_date, to_date]).aggregate(Sum('price'))['price__sum'] or 0
            order_items = OrderItem.objects.filter(is_deleted=False, date_added__range=[from_date, to_date])
            print("First",total_without_tax)

        total_cgst = 0
        total_igst = 0
        total_sgst = 0
        total_including_tax = 0

        for i in order_items:

            # only take the products belongs to hsn
            if i.product_variant.product.gst_code.type in "hsn":
                cgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.cgst_rate)
                sgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.sgst_rate)
                igst = i.price / decimal.Decimal(i.product_variant.product.gst_code.igst_rate)

                total_cgst += cgst
                total_igst += igst
                total_sgst += sgst

        total_including_tax = total_without_tax + total_sgst + total_cgst + total_igst

    except Exception as e:
        print(
            type(e).__name__,
            __file__,
            e.__traceback__.tb_lineno
        )
        print("Error ==>>",e)
        response_data = {"status": False, "message": str(e)}

    else:
        response_data = {"status": True, "total_without_tax": total_without_tax,
                         "total_including_tax": total_including_tax, "cgst": total_cgst, "sgst": total_sgst,
                         "igst": total_igst, }

    return response_data


def get_sac_totals(request):
    """
    get all the sac totals
    :param request:
    :return:
    """
    response_data = {}
    try:

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # order items total price
        total_without_tax = OrderItem.objects.aggregate(Sum('price'))['price__sum'] or 0

        # order items
        order_items = OrderItem.objects.filter(is_deleted=False)

        total_cgst = 0
        total_igst = 0
        total_sgst = 0
        total_including_tax = 0

        # if dates
        if from_date and to_date:
            from_date = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
            to_date = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

            total_without_tax = OrderItem.objects.filter(date_added__range=[from_date, to_date]).aggregate(Sum('price'))['price__sum'] or 0
            order_items = OrderItem.objects.filter(is_deleted=False, date_added__range=[from_date, to_date])
            print("second===>>",total_without_tax)
        for i in order_items:

            # only take the products belongs to hsn
            if i.product_variant.product.gst_code.type in "sac":
                cgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.cgst_rate)
                sgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.sgst_rate)
                igst = i.price / decimal.Decimal(i.product_variant.product.gst_code.igst_rate)

                total_cgst += cgst
                total_igst += igst
                total_sgst += sgst

        total_including_tax = total_without_tax + total_sgst + total_cgst + total_igst

    except Exception as e:
        print(
            type(e).__name__,
            __file__,
            e.__traceback__.tb_lineno
        )
        response_data = {"status": False, "message": str(e)}

    else:
        response_data = {"status": True, "total_without_tax": total_without_tax,
                         "total_including_tax": total_including_tax, "cgst": total_cgst, "sgst": total_sgst,
                         "igst": total_igst, }

    return response_data
