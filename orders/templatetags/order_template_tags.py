from django import template

register = template.Library()
from orders.models import Order


@register.simple_tag
def get_order_total(order_pk):
    """
    calculation of order total
    :param order_pk:
    :return:
    """
    order_instance = Order.objects.get(pk=order_pk)
    total = 0
    total += order_instance.total_amt

    if order_instance.courier_service_charge:
        total += order_instance.courier_service_charge

    if order_instance.discount:
        total -= order_instance.discount

    total += order_instance.tax_price

    return round(total)
