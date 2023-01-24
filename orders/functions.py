from django.db.models import Sum, F,FloatField
from orders.models import CouponStatus,OrderItem
from users.models import ShoppingBagItem

def get_coupon_amt(user,amount):
    returned_amt = 0

    cart_total = ShoppingBagItem.objects.filter(customer__user=user).aggregate(
        total=Sum(F('product_variant__price') * F('qty'), output_field=FloatField())
    )['total']

    print("cart total==>>", cart_total)

    if CouponStatus.objects.filter(customer__user=user, is_applied=True, status=False).exists():
        coupon = CouponStatus.objects.filter(customer__user=user, is_applied=True, status=False).first()
        percentage = int(coupon.coupon.offer_percentage)

        returned_amt = amount * percentage / 100

        coupon.status=True
        coupon.save()

    return returned_amt

# 4050,810,810


# get_delivery_amount()

def get_total_cgst_and_sgst(order_id):
    """
    getting the cgst and gst totals from order
    :param order_id:
    """
    order_items = OrderItem.objects.filter(order__id=order_id)
    total_cgst = 0
    total_sgst = 0

    for order_item in order_items:

        # rate of percentage calculation
        cgst_rate = order_item.product_variant.product.gst_code.cgst_rate
        product_price = order_item.product_variant.price
        cgst_amount = product_price * (cgst_rate / 100)
        total_cgst += cgst_amount

        sgst_rate = order_item.product_variant.product.gst_code.sgst_rate
        product_price = order_item.product_variant.price
        sgst_amount = product_price * (sgst_rate / 100)
        total_sgst += sgst_amount

    return {"cgst": total_cgst, "sgst": total_sgst, }
