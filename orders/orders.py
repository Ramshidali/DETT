from api.v1.general.functions import get_user
from api.v1.orders.serializers import OrderItemSerializer2
from customers.models import Moments,DeliveryDateTemp
from django.db.models import F, Sum, FloatField
from general.functions import get_auto_id
from orders.functions import get_coupon_amt
from orders.models import Order, OrderItem
from users.models import ShoppingBagItem
from api.v1.general.functions import clear_cart, update_cuopon_status
from api.v1.general.functions import calculate_gst

class   OrderManager:
    """
    class for getting order details
    """

    def __init__(self, order_id=None):
        self.order_id = order_id
        self.order_instance = 0
        if order_id:
            self.order_instance = Order.objects.get(pk=order_id)

    def get_order_address(self):
        """
        delivery address
        :return:
        """
        order_instance = self.order_instance
        address_data = {
            "name": order_instance.billing_name,
            "phone": order_instance.billing_phone,
            "address": order_instance.get_address(),
            "landmark": order_instance.billing_landmark
        }
        return address_data

    def get_ordered_items(self, request):
        """
        get customer ordered items
        """
        order_instance = self.order_instance
        order_items = OrderItem.objects.filter(order=order_instance)

        serialized = OrderItemSerializer2(order_items, many=True, context={"request": request})

        return serialized.data

    def get_orderd_totals(self):
        order_instance = self.order_instance
        total = order_instance.total_amt
        discount = order_instance.discount
        tax_total = order_instance.tax_price
        delivery_charges = order_instance.courier_service_charge
        grand_total = round(total - discount + delivery_charges + tax_total)
        tax_amount = order_instance.tax_price

        return {
            "total": total,
            "discount": discount,
            "delivery_charges": delivery_charges,
            "grand_total": grand_total,
            "tax_amount": tax_amount
        }

    def place_order(self, order_serialized=None, request=None):
        """
        => order placing
        :param order_serialized:
        :param request:
        """
        auto_id = get_auto_id(Order)
        creator = request.user
        updater = request.user
        customer = get_user(request.user)

        # due date
        delivery_date = DeliveryDateTemp.objects.filter(customer=customer).order_by('-date').first()

        # change after only payment gateway integration
        transaction_id = '5454545454'
        payment_order_id = '45454545454'

        # customer cart
        cart_total = ShoppingBagItem.objects.filter(customer=customer).aggregate(
            total=Sum(F('product_variant__price') * F('qty'), output_field=FloatField())
        )['total']

        # calculating gst
        gst_amt = calculate_gst(request.user)
        gst_totals = gst_amt['tax']

        print("GST ==>>",gst_totals)

        cart_and_gst_total = cart_total + float(gst_totals)

        # coupon applied amount
        coupon_amt = get_coupon_amt(request.user,cart_and_gst_total)
        print("COupon amoutn===>>>",coupon_amt)

        grand_total = cart_total

        invoice_id = f"DT2223/{str(auto_id).zfill(4)}"

        # order saving
        placed_order = order_serialized.save(
            auto_id=auto_id, creator=creator, updater=updater, customer=customer,
            transaction_id=transaction_id, payment_order_id=payment_order_id,
            delivery_date=delivery_date, total_amt=grand_total, discount=coupon_amt,
            invoice_id=invoice_id,tax_price=gst_totals
        )

        # if coupon applied clears all
        customer = get_user(request.user)
        update_cuopon_status(customer)

        return placed_order

    def save_order_items(self, user, order):
        """
        save and clear order items
        :param user:
        :param order:
        :return:
        """
        customer = get_user(user)

        return clear_cart(customer, order)

    def get_order_details(self):
        """
        fetching the full order model fields
        :return:
        """
        order = self.order_instance

        return order

    def get_order_items_for_invoice(self):
        order_items = OrderItem.objects.filter(order=self.order_instance)
        return order_items

    def get_invoice_id(self):
        return self.order_instance.invoice_id