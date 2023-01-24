import decimal
from api.v1.general.functions import get_user, update_cuopon_status,get_single_total_amount
from customers.models import Moments, DeliveryDateTemp
from general.functions import get_auto_id
from general.models import Extras
from orders.models import Order, OrderItem, OrderStatus
from products.models import ProductVariant
from orders.models import CouponStatus


class ProductVariantDetails:
    """
    get the details related to product variant
    """

    def __init__(self, product_variant_pk):
        self.product_variant_pk = product_variant_pk
        self.product_variant_instance = ProductVariant.objects.get(pk=self.product_variant_pk)
        self.product = self.product_variant_instance.product

    def get_product_variant(self):
        """
        only get the single product varint instance using given pk
        :return: model-query instance
        """
        return self.product_variant_instance

    def get_single_order_amounts(self, qty, user):
        """
        amt including discount and product qty total
        :param user:
        :param qty:
        :return:
        """
        special_discount = Extras.objects.filter().first().special_discount
        product_mrp = self.product_variant_instance.price
        total_amt = decimal.Decimal(product_mrp) * int(qty)
        discounted_price = 0
        coupon_amt = 0
        price_after_discount = 0
        is_coupon = False
        coupon_details = {}

        # gst and normal price calucaltion
        totals = get_single_total_amount(self.product_variant_instance,qty)
        print("=+++...",totals)
        gst_total = totals['gst']
        product_total = totals['product_total']
        total_amt = float(gst_total) + float(product_total)

        print("================")

        totals = {"total_amt": str(product_total), "gst": gst_total, "discount_amt": coupon_amt,
                  "final_total": total_amt,"delivery_charge": "0","is_coupon":is_coupon,"coupon_details":coupon_details}

        # check for applied coupons and deduct that amount also
        if CouponStatus.objects.filter(customer__user=user, is_applied=True, status=False, is_deleted=False).order_by(
                '-date_added').exists():
            instance = CouponStatus.objects.filter(customer__user=user, is_applied=True, status=False,
                                                   is_deleted=False).order_by('-date_added').first()

            # coupon percentage
            percentage = instance.coupon.offer_percentage
            is_coupon = True


            # if discount price is 0 it will take normal total amount
            # if price_after_discount is 0:
            #     coupon_applied_price = (total_amt * int(percentage)) / 100
            #     coupon_applied_price_after_discount = total_amt - coupon_applied_price
            #
            # else:
            #     coupon_applied_price = price_after_discount * (int(percentage) / 100)
            #     coupon_applied_price_after_discount = price_after_discount - coupon_applied_price

            coupon_applied_price = (total_amt * int(percentage)) / 100
            coupon_applied_price_after_discount = total_amt - coupon_applied_price

            print("coupon applied price==>>",coupon_applied_price)
            print("after discount==>>", coupon_applied_price_after_discount)
            print("Percent==>>", percentage)
            print("total amount ==>>", total_amt)

            coupon_amt = coupon_applied_price

            coupon_details = {
                "pk": instance.coupon.pk,
                "title": instance.coupon.coupon_code,
            }

            totals = {"total_amt": str(product_total), "gst": gst_total, "discount_amt": coupon_amt,
                      "final_total": coupon_applied_price_after_discount,"delivery_charge": "0","is_coupon":is_coupon,"coupon_details":coupon_details}

        return totals

    def place_single_order(self, request=None, serialized_value=None):
        """
        This functions includes :-
            => if any coupon applied the coupon will be updated
            => create the order item
            => create the order status
            => save this order
            => reduce Stock
        :param serialized_value:
        :param request:
        """

        auto_id = get_auto_id(Order)
        creator = request.user
        updater = request.user
        customer = get_user(request.user)
        transaction_id = '5454545454'
        payment_order_id = '45454545454'
        qty = request.data['qty']

        product_variant = self.product_variant_instance

        if product_variant:
            # getting the selected due date
            delivery_date = DeliveryDateTemp.objects.filter(customer__user=request.user).order_by('-date').first()

            invoice_id = f"DT2223/{str(auto_id).zfill(4)}"

            # the amounts
            product_variant_for_total = ProductVariantDetails(product_variant.pk)
            amounts = product_variant_for_total.get_single_order_amounts(qty, request.user)

            print("Discount in place order==>>",amounts['discount_amt'])
            # saving serializers value
            order = serialized_value.save(
                auto_id=auto_id, creator=creator, updater=updater, customer=customer,
                transaction_id=transaction_id, payment_order_id=payment_order_id,
                delivery_date=delivery_date,total_amt=amounts['total_amt'], discount=amounts['discount_amt'],
                invoice_id=invoice_id,
                tax_price=amounts['gst'],
            )

            # mark applied coupons as applied (STATUS=TRUE)
            update_cuopon_status(get_user(request.user))

            # order status created to track order
            # status 10 => pending
            OrderStatus.objects.create(status='10', order=order)

            OrderItem.objects.create(product_variant=product_variant, qty=qty, order=order,
                                     price=product_variant.price)

            # stock reduce
            product_variant.stock -= 1
            product_variant.save()

            return True

        else:
            return False
