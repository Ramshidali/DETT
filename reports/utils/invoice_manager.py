from orders.functions import get_total_cgst_and_sgst
from orders.models import OrderItem

class InvoiceManager:
    def __init__(self, order):
        self.order = order

    def get_invoice_totals(self):
        order_instance = self.order
        total_amt = order_instance.total_amt
        courier_service_charge = 0
        promotional_discount = 0

        if order_instance.courier_service_charge:
            courier_service_charge = order_instance.courier_service_charge

        gst_totals = get_total_cgst_and_sgst(order_instance.id)

        return {
            "courier_service_charge": courier_service_charge,
            "promotional_discount": promotional_discount,
            "gst_totals": gst_totals,
        }
