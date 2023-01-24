from decimal import Decimal

from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Count

register = template.Library()

from orders.models import *

@register.simple_tag
def get_order_total(order):
    total = 0
    if OrderItem.objects.filter(order__pk=order).exists():
        order_item_instance = OrderItem.objects.filter(order__pk=order)

        for i in order_item_instance:
            total += i.price
    return round(total)


@register.simple_tag
def get_percent(value,percent):

    # calc = value//percent
    return 0


@register.simple_tag()
def get_net_price(qty, price, sgst_percent,cgst_percent):

    # percentage amount
    cgst_rate = price * (cgst_percent /100)
    sgst_rate = price * (sgst_percent /100)

    total_price = Decimal(qty) * Decimal(price)

    grand_total_price = total_price + cgst_rate + sgst_rate

    return grand_total_price


@register.simple_tag()
def get_grand_total(order_total, promotional_discount, cgst, sgst, courier_service_charge):
    
    totals = Decimal(order_total) + Decimal(sgst) + (Decimal(cgst)) + (Decimal(courier_service_charge)) 

    return totals


@register.simple_tag()
def get_table_total(cgst,sgst):

    total = cgst + sgst
    return round(total,2)
    # return format(total, 'f')
    

@register.simple_tag()
def get_single_tax_cgst(price,gst_percent):
    
    totals = price * (gst_percent /100) 

    return totals


@register.simple_tag()
def get_single_tax_sgst(price,gst_percent):
    
    totals = price * (gst_percent /100) 

    return totals