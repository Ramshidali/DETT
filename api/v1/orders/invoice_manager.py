from orders.models import Order


class InvoiceManager:
    def __init__(self,order_id):
        self.order_id = order_id
        self.order_instance = Order.objects.get(pk=order_id)
