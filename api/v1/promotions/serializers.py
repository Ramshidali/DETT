import decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from general.functions import get_auto_id
from products.models import ProductVariant, ProductImage
from promotions.models import Enquiry
from rest_framework import serializers


class PVSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    image_slider = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['title', 'mrp', 'price', 'description', 'image', 'offer', 'id', 'image_slider']

    def get_description(self, instances):
        return instances.product.product_description

    def get_image(self, instances):
        request = self.context.get('request')
        image = ProductImage.objects.filter(product_variant=instances).first()
        if image:
            return request.build_absolute_uri(image.feautured_image.url)

        return None

    def get_offer(self, instances):
        mrp = instances.mrp
        price = instances.price
        offer = price / mrp * 100
        return offer

    def get_image_slider(self, instances):
        request = self.context.get("request")
        images = ProductImage.objects.filter(product_variant=instances)
        sliders = []
        for i in images:
            sliders.append(request.build_absolute_uri(i.feautured_image.url))

        return sliders


class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = Enquiry
        exclude = ['enquiry_id','auto_id']


class EnquiryViewSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = '__all__'

    def get_product(self, instances):
        request = self.context.get("request")
        product = ProductVariant.objects.get(pk=instances.product.pk)
        serialized = PVSerializer(product,context={"request": request})
        return serialized.data
