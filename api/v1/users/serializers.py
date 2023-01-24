from datetime import datetime, timedelta

import decimal
from api.v1.general.functions import get_otp, get_total_amount
from api.v1.general.functions import get_user
from api.v1.orders.serializers import ProductImageSerializer
from customers.models import Customer
from customers.models import CustomerAddress, MomentCard
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Max
from general.functions import get_auto_id
from general.models import SetDueDays, SetCoupon, Slider
from products.models import ProductVariant, ProductForOccassion, Occassion, SubOccassion, PersonType, ProductImage, \
    UnitOfMeasurement, Unit, Product
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from users.models import ShoppingBagItem
from orders.models import CouponStatus
from customers.models import DeliveryDateTemp


class OccassionSerializer(serializers.ModelSerializer):
    sub_occassion = serializers.SerializerMethodField()

    class Meta:
        model = Occassion
        fields = '__all__'

    def get_sub_occassion(self, instances):
        request = self.context.get("request")
        occassion_id = instances.pk
        occassion = SubOccassion.objects.filter(occassion=occassion_id, is_deleted=False)
        occassion_serialized = SubOccassionSerializer(occassion, many=True, context={"request": request})
        return occassion_serialized.data


class ProductOccassionSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    mrp = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    occassion = serializers.SerializerMethodField()
    sub_occassion = serializers.SerializerMethodField()

    class Meta:
        model = ProductForOccassion
        fields = ['product_name', 'mrp', 'price', 'occassion', 'sub_occassion']

    def get_product_name(self, instances):
        if instances.product_variant.title:
            return instances.product_variant.title
        else:
            return ""

    def get_mrp(self, instances):
        if instances.product_variant.mrp:
            return instances.product_variant.mrp
        else:
            return ""

    def get_price(self, instances):
        if instances.product_variant.price:
            return instances.product_variant.price
        else:
            return ""

    def get_occassion(self, instances):
        if instances.occassion.occassion:
            return instances.occassion.occassion
        else:
            return ""

    def get_sub_occassion(self, instances):
        if instances.sub_occassion.sub_occassion:
            return instances.sub_occassion.sub_occassion
        else:
            return ""


class SubOccassionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOccassion
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ['customer']


class DueDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetDueDays
        fields = ['no_of_days', ]


class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['feautured_image', ]


class VariantSerializer(serializers.ModelSerializer):
    unit_name = serializers.SerializerMethodField()
    uom_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    product_name  = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        exclude = ['creator', 'updater', 'date_added', 'date_updated', 'is_deleted', 'opening_stock',
                   'stock', ]

    def get_unit_name(self, instances):
        if instances.unit.unit:
            return instances.unit.unit
        else:
            return ""

    def get_product_name(self,instances):
        return instances.get_full_name()

    def get_uom_name(self, instances):
        if instances.uom.unit_of_measurement:
            return instances.uom.unit_of_measurement
        else:
            return ""

    def get_image(self, instances):
        product_instances = Product.objects.get(pk=instances.product.pk)
        print(product_instances)
        request = self.context.get("request")
        image = product_instances.feautured_image
        serialized = VariantImageSerializer(product_instances,context={"request": request})
        return serialized.data

    def get_meta_description(self, instances):
        if instances.product.meta_description:
            return instances.product.meta_description
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


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['unit', 'pk']


class SingleProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = ['unit_of_measurement', 'pk']


class ProductVariantSearchSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        exclude = ['creator', 'updater', 'date_added', 'date_updated', 'is_deleted', 'age_group']

    def get_image(self, instances):
        product_instances = Product.objects.get(pk=instances.product.pk)
        print(product_instances)
        request = self.context.get("request")
        serialized = ProductImageSerializer(product_instances, context={"request": request})
        return serialized.data

    def get_offer(self, instances):
        mrp = instances.mrp
        price = instances.price
        offer = price / mrp * 100
        return offer


class VariantSizeSerializer(serializers.ModelSerializer):
    # size = serializers.SerializerMethodField()

    class Meta:
        model = UnitOfMeasurement
        fields = ['unit_of_measurement']

    def get_description(self, instances):
        if instances.product.product_description:
            return instances.product.product_description
        else:
            return ""


class VariantSwitchSerializer(serializers.ModelSerializer):
    # serializer for product single view , cart product switching
    offer = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = ['pk', 'title','is_default','unit','mrp','price','offer','images']

    def get_offer(self, instances):
        mrp = instances.mrp
        price = instances.price
        offer = (mrp - price) / mrp * 100
        return offer
    
    def get_images(self, instances):
        request = self.context.get("request")
        img = []
        images = ProductImage.objects.filter(product_variant=instances)
        images_serialized = VariantImageSerializer(images, many=True, context={"request": request})
        for images in images_serialized.data:
            print(images)
            img.append(images['feautured_image'])
        return img

class ProductVariantSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()
    pincode = serializers.SerializerMethodField()
    product_full_name = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        exclude = ['creator', 'updater', 'date_added', 'date_updated', 'is_deleted', 'age_group', ]

    def get_variants(self, instance):
        request = self.context.get("request")
        product_variant_instances = ProductVariant.objects.filter(product=instance.product,is_deleted=False)

        variants_serialized = VariantSwitchSerializer(product_variant_instances, many=True, context={"request": request})
        return variants_serialized.data

    def get_images(self, instances):
        request = self.context.get("request")
        img = []
        images = ProductImage.objects.filter(product_variant=instances)
        images_serialized = VariantImageSerializer(images, many=True, context={"request": request})
        for images in images_serialized.data:
            print(images)
            img.append(images['feautured_image'])
        return img

    def get_meta_description(self, instances):
        if instances.product.meta_description:
            return instances.product.meta_description
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

    def get_due_date(self, instances):
        date = ''
        request = self.context.get("request")
        if Customer.objects.filter(user=request.user).exists():
            customer= Customer.objects.get(user=request.user)
            
            # print(customer.pk, "user exists")
            due_date = DeliveryDateTemp.objects.filter(customer=customer).first()
            date = due_date.date
        
        return date

    def get_pincode(self, instances):
        user = self.context.get("request").user
        customer = get_user(user)

        if CustomerAddress.objects.filter(is_default=True, customer=customer).exists():
            pincode = CustomerAddress.objects.get(is_default=True, customer=customer)

            return pincode.pincode

    def get_product_full_name(self,instance):
        return instance.get_full_name()
    
    def get_unit(self, instance):
        unit = instance.unit.unit

        return str(unit)
    
    def get_uom(self, instance):
        uom = instance.uom.unit_of_measurement
        return str(uom)


class CartVariantSerializer(serializers.ModelSerializer):
    # serializer for cart with cart item default
    is_carted =serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['pk', 'title','is_default','is_carted']

    def get_is_carted(self,instance):
        request = self.context.get("request")
        is_carted = False
        if ShoppingBagItem.objects.filter(customer__user=request.user,product_variant=instance).exists():
            is_carted = True
            return is_carted
        else:
            return is_carted

class CartSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    variant_name = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    mrp = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingBagItem
        fields = '__all__'

    def get_variant_name(self, instance):
        if instance.product_variant.title:
            return instance.product_variant.get_full_name()
        else:
            return ""

    # def get_variants(self, instance):
    #     pro = ProductVariant.objects.filter(product=instance.product_variant.product)
    #     print("Prod====>", pro)
    #     product_id = instance.product_variant.product.pk
    #     variants = Unit.objects.filter(unit_of_measurement=instance.product_variant.uom)
    #     variants_serialized = SizeSerializer(variants, many=True)
    #     return variants_serialized.data

    def get_variants(self, instance):
        request = self.context.get('request')
        variant_instances = ProductVariant.objects.filter(product=instance.product_variant.product)
        variants_serialized = CartVariantSerializer(variant_instances, many=True, context={"request": request})

        return variants_serialized.data

    def get_images(self, instances):
        request = self.context.get("request")
        img = []
        images = ProductImage.objects.filter(product_variant=instances.product_variant)
        images_serialized = VariantImageSerializer(images, many=True, context={"request": request})
        for images in images_serialized.data:
            print(images)
            img.append(images['feautured_image'])
        return img

    def get_meta(self, instances):
        if instances.product_variant.product.meta_description:
            return instances.product_variant.product.meta_description
        else:
            return ""

    def get_mrp(self, instances):
        if instances.product_variant.mrp:
            return instances.product_variant.mrp
        else:
            return ""

    def get_price(self, instances):
        if instances.product_variant.price:
            return instances.product_variant.price
        else:
            return ""

    def get_offer(self, instances):
        mrp = instances.product_variant.mrp
        price = instances.product_variant.price
        offer = (mrp - price) / mrp * 100
        return offer

    def get_size(self, instance):
        if instance.product_variant.unit.unit:
            return instance.product_variant.unit.unit
        else:
            return ""

    def get_due_date(self, instances):
        request = self.context.get("request")
        due_date = DeliveryDateTemp.objects.filter(customer__user=request.user).first()

        return due_date.date


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = ['is_deleted', 'auto_id', 'unit_of_measurement']


class ChangeQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingBagItem
        fields = ['qty', ]


class ChangeSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingBagItem
        fields = ['product_variant', ]

    def change_size(self, instance, validated_data):
        product = None
        id = instance.id
        brand = instance.product_variant.brand
        product = instance.product_variant.product
        unit = instance.product_variant.unit

        if ProductVariant.objects.filter(brand=brand, product=product, unit=unit).exists():
            product = ProductVariant.objects.filter(brand=brand, product=product, unit=unit).first()
            size = ShoppingBagItem.objects.filter(pk=id).update(product_variant=product, qty=1)
            return size


class GetCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetCoupon
        fields = ['coupon_code', 'pk', 'title', 'description']


class CouponSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    # total_price = serializers.SerializerMethodField()
    # discount = serializers.SerializerMethodField()

    class Meta:
        model = SetCoupon
        fields = ['coupon_code', 'percentage', ]

    def get_percentage(self, instances):
        return instances.offer_percentage

    def get_total_price(self, instances):
        request = self.context.get('request')
        user = self.context.get("request").user
        customer = get_user(user)
        total_amount = request.data.get("total_amount")

        # amt = get_total_amount(customer)
        discounted_price = decimal.Decimal(float(total_amount)) * decimal.Decimal(
            float(instances.offer_percentage)) / 100
        total = decimal.Decimal(float(total_amount)) - discounted_price
        return total

    def get_discount(self, instances):
        request = self.context.get('request')
        user = self.context.get("request").user
        customer = get_user(user)
        discount = request.data.get("discount_price")
        total_amount = request.data.get("total_amount")
        discounted = decimal.Decimal(float(total_amount)) * decimal.Decimal(float(instances.offer_percentage)) / 100
        discounted_price = discounted + decimal.Decimal(float(discount))

        return discounted_price


class OccassionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occassion
        fields = ['occassion', 'id']


class PersonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonType
        fields = ['person_type', 'id']


class OccassionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occassion
        fields = ['occassion_image', ]


class MomentCardSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = MomentCard
        exclude = ['customer', 'date_added', 'is_deleted']

    def get_person(self, instances):
        if instances.person_type.person_type:
            return instances.person_type.person_type
        else:
            return ""

    def get_image(self, instances):
        request = self.context.get("request")
        if instances.occassion.occassion_image.url:
            images = Occassion.objects.get(pk=instances.occassion.pk)
            images_serialized = OccassionImageSerializer(images, context={"request": request})

            return images_serialized.data['occassion_image']
        else:
            return ""


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['title', 'image']
