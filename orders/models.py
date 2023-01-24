from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

from customers.models import Customer, Moments,DeliveryDateTemp
from delivery_agents.models import DeliveryAgent
from general.models import BaseModel, UserBaseModel, SetCoupon
from products.models import ProductVariant, GstCodes


ORDER_CHOICES = (
    ("10", 'Ordered'),
    ("20", 'Packed'),
    ("30", 'Shipped'),
    ("40", 'Out for delivery'),
    ("50", 'Delivered'),
    ("0", 'Cancelled'),
)

PAYMENT_METHOD_CHOICES = (
    ("cod", 'Cash on delivery'),
    ("gpay", 'Google Pay'),
    ("phone_pe", 'Phone Pe'),
    ("upi", 'UPI'),
)

PAYMENT_CHOICES = (
    ("10", 'pending'),
    ("20", 'Paid'),
    ("30", 'Failed'),
)

class Order(BaseModel):
    billing_name = models.CharField(max_length=256, null=False)
    billing_phone = models.CharField(max_length=10, null=False)
    billing_address = models.TextField(max_length=256, null=True, blank=True)
    billing_street = models.CharField(max_length=256, null=False)
    billing_landmark = models.CharField(max_length=256, null=False)
    billing_city = models.CharField(max_length=256, null=False)
    billing_state = models.CharField(max_length=256, null=False)
    pincode = models.CharField(max_length=16, null=True, blank=True)
    discount = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, validators=[
                                MinValueValidator(Decimal('0.00'))], )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    order_status = models.CharField(max_length=256, null=False, default="10",choices=ORDER_CHOICES)
    total_amt = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, validators=[
                                MinValueValidator(Decimal('0.00'))])
    payment_method = models.CharField(max_length=256, null=False,choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=256, null=False,choices=PAYMENT_CHOICES)
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.CASCADE, null=True, blank=True)
    card_name = models.CharField(max_length=256, null=True, blank=True)
    card_number = models.CharField(max_length=256, null=True, blank=True)
    transaction_id = models.CharField(max_length=256, null=True, blank=True)
    payment_order_id = models.CharField(max_length=256, null=True, blank=True)
    delivery_date = models.ForeignKey(DeliveryDateTemp, on_delete=models.CASCADE, null=True, blank=True)
    courier_service_charge = models.PositiveIntegerField(default=0)
    sac_code = models.ForeignKey(GstCodes, on_delete=models.CASCADE, null=True, blank=True)
    invoice_id = models.CharField(max_length=256, null=True, blank=True)
    tax_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, validators=[
                                MinValueValidator(Decimal('0.00'))],null=True,blank=True)

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def get_address(self):
        return f"{self.billing_name}, {self.billing_city}, {self.billing_state}, {self.pincode}"

    def __str__(self):
        return self.billing_name


class OrderItem(UserBaseModel):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, )
    qty = models.CharField(max_length=256, null=True, blank=True)

    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                validators=[MinValueValidator(Decimal('0.00'))])
    order = models.ForeignKey(Order, on_delete=models.CASCADE, )

    class Meta:
        ordering = ('qty',)
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self):
        return str(self.qty)


class OrderStatus(models.Model):
    status = models.CharField(max_length=256, choices=ORDER_CHOICES)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, )
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
        verbose_name = 'order status'
        verbose_name_plural = 'order statuses'

    def __str__(self):
        return str(self.order)




class OrderReview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, )
    star = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'order review'
        verbose_name_plural = 'order reviews'

    def __str__(self):
        return str(self.order.customer.name)



class CouponStatus(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    is_applied = models.BooleanField()
    coupon = models.ForeignKey(SetCoupon, on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'coupon status'
        verbose_name_plural = 'coupon status'

    def __str__(self):
        return str(self.customer.name)