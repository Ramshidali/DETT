from django.contrib import admin
from orders.models import OrderItem, Order, OrderStatus, OrderReview, CouponStatus

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(OrderReview)
admin.site.register(CouponStatus)