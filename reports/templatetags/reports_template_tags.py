from django.template import Library

import decimal

register = Library()
from django.db.models import Sum
from orders.models import Order, OrderItem


@register.simple_tag
def get_order_tax_details(order_id, type):
    """
    for calculating the total hsn on orders
    :param type:
    :param order_id:
    :return:
    """
    response_data = {}
    try:
        order_instances = Order.objects.get(pk=order_id)

        order_items = OrderItem.objects.filter(order=order_instances)
        order_items_total = OrderItem.objects.aggregate(Sum('price'))

        total_cgst = 0
        total_igst = 0
        total_sgst = 0

        total_including_tax = 0
        type_gst = None

        for i in order_items:
            # check the type of code ie hsn
            if type in "hsn":
                type_gst = "hsn_type"
                # only take the products belongs to hsn
                if i.product_variant.product.gst_code.type in "hsn":
                    cgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.cgst_rate)
                    sgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.sgst_rate)
                    igst = i.price / decimal.Decimal(i.product_variant.product.gst_code.igst_rate)

                    total_cgst += cgst
                    total_igst += igst
                    total_sgst += sgst

            # only take the product has sac code
            elif type in "sac":
                type_gst = "sac_type"
                # only take the products belongs to sac
                if i.product_variant.product.gst_code.type in "sac":
                    cgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.cgst_rate)
                    sgst = i.price / decimal.Decimal(i.product_variant.product.gst_code.sgst_rate)
                    igst = i.price / decimal.Decimal(i.product_variant.product.gst_code.igst_rate)

                    # all the values appended to the variable
                    total_cgst += cgst
                    total_igst += igst
                    total_sgst += sgst

        total_including_tax = order_items_total['price__sum'] + total_sgst + total_cgst + total_igst
        total_excluding_tax = total_including_tax - total_igst - total_sgst - total_cgst

    except Exception as e:
        response_data = {"error": str(e)}
    else:
        response_data = {"order_items_total": order_items_total['price__sum'], "cgst": total_cgst, "sgst": total_sgst,
                         "igst": total_igst, "total_including_tax": total_including_tax,
                         "total_excluding_tax": total_excluding_tax, "type": type_gst}

    return response_data


def get_final_report(from_date,to_date):
    """
    Get the totals of sales and gst relates
    """
    response_data = {}
    try:
        orders = Order.objects.filter(is_deleted=False)

    except Exception as e:
        pass
    else:
        pass

