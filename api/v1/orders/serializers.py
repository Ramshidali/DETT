from api.v1.general.functions import get_user, get_order_total, get_delivery_fee

from orders.models import Order, OrderItem, OrderStatus, OrderReview
from products.models import Product, ProductVariant, ProductImage, Unit
from rest_framework import serializers

from django.conf import settings
from customers.models import DeliveryDateTemp

media_url = settings.MEDIA_URL



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['order_status', 'customer', 'auto_id', 'creator', 'updater', 'date_added', 'date_updated',
                   'is_deleted', 'delivery_date']


class GetOrderSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    order_grand_total = serializers.SerializerMethodField()
    order_invoice_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ['order_status', 'customer', 'auto_id', 'creator', 'updater', 'date_added', 'date_updated',
                   'is_deleted']
        
    def get_id(self,instance):
        return str(instance.id)

    def get_items(self, instances):
        request = self.context.get("request")
        q = request.GET.get('q')
        customer = get_user(request.user)
        s = OrderItem.objects.filter(order=instances.id)

        if q:
            s = OrderItem.objects.filter(product_variant__title__icontains=q, order=instances.pk)

        serialized = OrderItemSerializer(s, many=True, context={"request": request})
        return serialized.data

    def get_order_date(self, instances):
        latest_date = OrderStatus.objects.filter(order=instances).first()
        date_added = instances.date_added.strftime("%d/%m/%Y")
        date_updated = instances.date_updated.strftime("%d/%m/%Y")

        if instances.order_status == "10" or instances.order_status == '20' or instances.order_status == '30' or instances.order_status == '40':
            return "Orderd on " + str(date_added)

        elif instances.order_status == '0':
            return "Cancelled on " + str(date_updated)
        else:
            return "Delivered on " + str(date_updated)

    def get_order_grand_total(self,instance):
        from orders.orders import OrderManager

        order_manager = OrderManager(order_id=instance.id)
        grand_total = order_manager.get_orderd_totals()['grand_total']
        return grand_total
    
    def get_order_invoice_id(self,instance):
        from orders.orders import OrderManager

        order_manager = OrderManager(order_id=instance.id)
        invoice_id = order_manager.get_invoice_id()
        return invoice_id


class OrderTrackSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    # status_name = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_status', 'billing_name', 'billing_state', 'billing_street', 'billing_landmark', 'phone',
                  'billing_phone', 'status', 'review','invoice_id']

    def get_phone(self, instances):
        return instances.customer.phone

    def get_status(self, instances):
        instances = OrderStatus.objects.filter(order=instances.pk)
        print("===> instances", instances)
        serialized = OrderDeliveryStatusSerializer(instances, many=True)
        return serialized.data

    def get_review(self, instances):
        instances_review = None
        if OrderReview.objects.filter(order=instances.pk).exists():
            instances_review = OrderReview.objects.filter(order=instances.pk).first()
            return instances_review.star
        else:
            return ""

    # def get_status_name(self,instances):
    #     instances = OrderStatus.objects.filter(order=instances.pk)
    #     print("===> instances",instances)
    #     serialized = OrderDeliveryStatusSerializer(instances, many=True)
    #     return serialized.data


class OrderDeliveryStatusSerializer(serializers.ModelSerializer):
    date_format = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatus
        fields = ['status','order','date','title','status_name','date_format']

    def get_date_format(self, instances):
        date = instances.date
        day_name = date.strftime("%A")
        year = date.strftime("%y")
        day = date.strftime("%d")
        month = date.strftime('%B')
        return str(day_name)[:3] + ',' + str(day) + ' ' + str(month)[:3] + ' ' + str(year)

    def get_status_name(self, instances):
        status = instances.status
        
        if status == '10':
            return 'Ordered'
        elif status == '20':
            return 'Packed'
        elif status == '30':
            return 'Shipped'
        elif status == '40':
            return 'Out for delivery'
        elif status == '50':
            return 'Delivered'
        elif status == '0':
            return 'Cancelled'

    def get_title(self, instances):
        status = instances.status
        print(type(status))
        if status == '10':
            return 'Your order has been placed'
        elif status == '20':
            return 'Seller has Processed your order'
        elif status == '30':
            return 'Your order has been shipped'
        elif status == '40':
            return 'Product Out for delivery'
        elif status == '50':
            return 'Your order has been delivered'
        elif status == '0':
            return 'your order has Cancelled'


class OrderWithAddressSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    delivery_charge = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ['order_status', 'customer', 'auto_id', 'creator', 'updater', 'date_added', 'date_updated',
                   'is_deleted', 'payment_method', 'payment_status', 'card_name', 'card_number', 'transaction_id',
                   'payment_order_id', 'delivery_agent']

    def get_items(self, instances):
        request = self.context.get("request")
        s = OrderItem.objects.filter(order=instances.id)
        print(s)
        serialized = OrderSingleSerializer(s, many=True, context={"request": request})
        return serialized.data

    def get_order_date(self, instances):
        date = instances.date_added.strftime("%d/%m/%Y")
        if instances.order_status == "10" or instances.order_status == '20' or instances.order_status == '30':
            return "Ordered on " + str(date)
        else:
            return "Delivered on " + str(date)

    def get_total(self, instances):
        price = get_order_total(instances.pk)
        return price

    def get_discount(self, instances):
        total = get_order_total(instances.pk)
        ordered_price = instances.total_amt
        discount = total - ordered_price
        return discount

    def get_delivery_charge(self, instances):
        charge = get_delivery_fee(instances.customer)
        return charge


class OrderListItemsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    total_amt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'items', 'total_amt']

    def get_items(self, instances):
        request = self.context.get("request")
        s = OrderItem.objects.filter(order=instances.id)
        serialized = OrderItemSerializer(s, many=True, context={"request": request})
        return serialized.data

    def get_total_amt(self, instances):
        s = OrderItem.objects.filter(order=instances.id)
        price = 0
        for items in s:
            price = items.price

        return price

    def get_order_date(self, instances):
        s = OrderItem.objects.filter(order=instances.id)
        serialized = OrderItemSerializer(s, many=True)
        for i in serialized.data:
            return i['order_status']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['feautured_image', ]


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_status(self, instances):
        date = instances.date_added.strftime("%d/%m/%Y")
        if instances.order_status == "10" or instances.order_status == '20' or instances.order_status == '30':
            return "Ordered on " + str(date)
        else:
            return "Delivered on " + str(date)

    def get_order_items(self, instance):
        instances = OrderItem.objects.filter(order=instance)
        serialized = OrderItemSerializer2(instances, many=True)

        return serialized.data


class OrderItemSerializer2(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        exclude = ['is_deleted']

    def get_name(self,instance):
        return instance.product_variant.get_full_name()

    def get_description(self,instance):
        return instance.product_variant.product.meta_description

    def get_image(self,instance):
        product = instance.product_variant.product
        request = self.context.get("request")
        serialized = ProductImageSerializer(product,context={"request":request})
        return serialized.data


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['feautured_image', ]


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        exclude = ['is_deleted']

    def get_order_status(self, instances):
        user = self.context.get("request").user
        print("===>> user", user)
        customer = get_user(user)
        orders = Order.objects.filter(customer=customer, pk=instances.order.id)
        serialized = OrderStatusSerializer(orders, many=True)
        return serialized.data

    def get_name(self, instances):
        if instances.product_variant.get_full_name:
            return instances.product_variant.get_full_name()
        else:
            return ""

    def get_image(self, instances):
        product_instances = ProductImage.objects.filter(product_variant=instances.product_variant.id).first()
        print(product_instances)
        request = self.context.get("request")
        serialized = ProductVariantImageSerializer(product_instances, context={"request": request})
        return serialized.data

    def get_meta(self, instances):
        if instances.product_variant.product.meta_description:
            return instances.product_variant.product.meta_description
        else:
            return ""


class OrderSingleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        exclude = ['is_deleted']

    def get_order_status(self, instances):
        user = self.context.get("request").user
        print("===>> user", user)
        customer = get_user(user)
        orders = Order.objects.filter(customer=customer, pk=instances.order.id)
        serialized = OrderSerializer(orders, many=True)
        return serialized.data

    def get_name(self, instances):
        if instances.product_variant.title:
            return instances.product_variant.title
        else:
            return ""

    def get_image(self, instances):
        product_instances = ProductImage.objects.filter(product_variant=instances.product_variant.pk).first()
        print(product_instances)
        request = self.context.get("request")
        serialized = ProductVariantImageSerializer(product_instances, context={"request": request})
        return serialized.data

    def get_meta(self, instances):
        if instances.product_variant.product.meta_description:
            return instances.product_variant.product.meta_description
        else:
            return ""


class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['feautured_image', ]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['unit', 'pk']


class SingleOrderVariantSerializer(serializers.ModelSerializer):
    # serializer for cart with cart item default

    class Meta:
        model = ProductVariant
        fields = ['pk', 'title',]





class ProductVariantSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    delivery_date = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        exclude = ['creator', 'updater', 'date_added', 'date_updated', 'is_deleted', 'age_group', ]

    def get_variants(self, instance):
        request = self.context.get('request')
        variant_instances = ProductVariant.objects.filter(product=instance.product)
        variants_serialized = SingleOrderVariantSerializer(variant_instances, many=True, context={"request": request})

        return variants_serialized.data

    def get_image(self, instances):
        product = instances.product
        request = self.context.get("request")
        serialized = ProductImageSerializer(product, context={"request": request})
        return serialized.data

    def get_meta_description(self, instances):
        if instances.product.meta_description:
            return instances.product.meta_description
        else:
            return ""

    def get_unit(self, instances):
        if instances.unit.unit:
            return instances.unit.unit
        else:
            return ""

    def get_description(self, instances):
        if instances.product.product_description:
            return instances.product.product_description
        else:
            return ""

    def get_offer(self, instances):
        mrp = instances.mrp
        price = instances.price
        offer = (mrp - price) / mrp * 100
        return offer

    def get_full_name(self,instance):
        return instance.get_full_name()

    def get_delivery_date(self,instance):
        request = self.context.get("request")
        due_date = DeliveryDateTemp.objects.filter(customer__user=request.user).first()

        return due_date.date


class OrderNotificationSerializer(serializers.ModelSerializer):
    date_format = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatus
        fields = '__all__'

    def get_status_name(self, instances):
        status = instances.status
        
        if status == "10":
            return 'Ordered'
        elif status == "20":
            return 'Packed'
        elif status == "30":
            return 'Shipped'
        elif status == "40":
            return 'Out for delivery'
        elif status == "50":
            return 'Delivered'
        elif status == "0":
            return 'Cancelled'

    def get_title(self, instances):
        status = instances.status
        
        if status == "10":
            return 'Your order has been placed'
        elif status == "20":
            return 'Seller has Processed your order'
        elif status == "30":
            return 'Your order has been shipped'
        elif status == "40":
            return 'Product Out for delivery'
        elif status == "50":
            return 'Your order has been delivered'
        elif status == "0":
            return 'your order has Cancelled'

    def get_date_format(self, instances):
        date = instances.date
        day_name = date.strftime("%A")
        year = date.strftime("%y")
        day = date.strftime("%d")
        month = date.strftime('%B')
        return str(day_name)[:3] + ',' + str(day) + ' ' + str(month)[:3] + ' ' + str(year)
