import decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from general.functions import get_auto_id
from products.models import ProductVariant, Product, ProductCategory, ProductColor, Brand, Unit,RecentSearches
from rest_framework import serializers
from general.models import GiftImage
from customers.models import DeliveryDateTemp


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['category_name',]


class SizeSerializer(serializers.ModelSerializer):
    
    uom =serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = "__all__"
        
    def get_uom(self,instance):
        return instance.unit_of_measurement.unit_of_measurement
        

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['color']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand']


class PVSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = "__all__"

    def get_color(self, instances):
        return instances.color.color


class SearchSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()


    class Meta:
        model = RecentSearches
        fields = ['product','image','name']

    def get_image(self, instances):
        request = self.context.get('request')

        photo_url = instances.product.product.feautured_image.url
        return request.build_absolute_uri(photo_url)

    def get_name(self, instances):
        return instances.product.title

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftImage
        fields = ['image',]


# get laetst delivery date serializer
class DeliveryDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryDateTemp
        fields = ['date',]