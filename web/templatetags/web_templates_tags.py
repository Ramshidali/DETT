from django import template
from django.urls import reverse

from products.models import ProductVariant

register = template.Library()


@register.filter
def get_offer_percent(instance):
    
    offer = (instance.mrp-instance.price) / instance.mrp
    offer_rate = offer * 100
    
    return offer_rate


@register.filter
def get_total_gst(pk):
    instance = ProductVariant.objects.get(pk=pk,is_deleted=False)
    
    total_cgst = 0
    total_sgst = 0
    total_igst = 0
    gst_total = 0
    total_price = 0
        
    cgst = instance.product.gst_code.cgst_rate / 100
    sgst = instance.product.gst_code.sgst_rate / 100
    igst = instance.product.gst_code.igst_rate / 100

     # appended to the totals gst fields
    total_cgst = total_cgst + cgst
    total_sgst = total_sgst + sgst
    total_igst = total_igst + igst

    # total igst removed needed to be added
    gst_total += total_cgst + total_sgst
    total_price = gst_total + instance.price
    # print(grand_total)
    
    return {
        "gst_total": gst_total,
        "total_price": total_price,
    }



@register.simple_tag
def anchor(url_name, section_id):
    return reverse(url_name) + '#' + section_id
