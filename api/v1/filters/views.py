import json
from api.v1.filters.serializers import CategorySerializer, ColorSerializer, BrandSerializer, PVSerializer,SearchSerializer,ImageSerializer,SizeSerializer
from api.v1.general.functions import generate_serializer_errors, get_total_amount, get_user
from api.v1.users.serializers import ProductVariantSerializer
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import (get_object_or_404, )
from django.shortcuts import (get_object_or_404, )
from general.functions import get_auto_id
from products.models import ProductVariant, ProductCategory, ProductColor, Brand, Unit
from general.models import GiftImage
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from products.models import RecentSearches
from customers.models import Customer, Moments,DeliveryDateTemp


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_category(request):
    category_instances = ProductCategory.objects.filter(is_deleted=False)
    color_instances = ProductColor.objects.filter(is_deleted=False)
    brand_instances = Brand.objects.filter(is_deleted=False)
    
    size_instances = Unit.objects.filter(is_deleted=False)
    serialized = SizeSerializer(size_instances, many=True, context={"request": request})

    category = {}
    category_obj = list(category_instances.values())
    category['data'] = category_obj

    color = {}
    color_obj = list(color_instances.values())
    color['data'] = color_obj

    brand = {}
    brand_obj = list(brand_instances.values())
    brand['data'] = brand_obj

    size = {}
    size_obj = list(size_instances.values())
    size['data'] = size_obj

    response_data = {
        "StatusCode": 6000,
        "category": category,
        "color": color,
        "brand": brand,
        "size": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_color(request):
    instances = ProductColor.objects.filter(is_deleted=False)
    serialized = ColorSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_brand(request):
    instances = Brand.objects.filter(is_deleted=False)
    serialized = BrandSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def apply_filter(request):
    instances = None
    instances = ProductVariant.objects.filter(is_deleted=False)

    size = request.GET.getlist('s')
    color = request.GET.getlist('c')
    brand = request.GET.getlist('b')
    cat = request.GET.getlist('cat')
    price1 = request.GET.get('p1')

    if color:
        instances = instances.filter(color__in=color)

    if brand:
        instances = instances.filter(brand__in=brand)

    if size:
        instances = instances.filter(uom__in=size)

    if cat:
        instances = instances.filter(product__product_category__in=cat)
    
    if price1:
        instances = instances.filter(price__in=price1)

    serialized = PVSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def save_search(request,pk):
    customer = get_user(request.user)
    auto_id = get_auto_id(RecentSearches)
    creator = request.user
    updater = request.user
    product = ProductVariant.objects.get(pk=pk)
    RecentSearches.objects.create(
        customer=customer,
        auto_id=auto_id,
        creator=creator,
        updater=updater,
        product=product
    )
    response_data = {
        "StatusCode": 6000,
        "message": "Sucess",
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def save_person(request):

    customer = get_user(request.user)
    name = request.data['name']
    date = request.data['date']

    Moments.objects.create(
        customer=customer,
        name=name,
        date=date,
    )
    response_data = {
        "StatusCode": 6000,
        "message": "Sucess",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def save_delivery_date(request):

    date = request.data['delivery_date']
    # customer = get_user(request.user)
    customer = Customer.objects.get(user=request.user)
    # print(date,"================>>>>+")
    # print(customer,"================>>>>+")
    DeliveryDateTemp.objects.create(
        customer=customer,
        date=date,
    )
    response_data = {
        "StatusCode": 6000,
        "message": "Sucess",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_search(request):
    customer = get_user(request.user)
    instances = RecentSearches.objects.filter(customer=customer).order_by('-date_added')[:4]
    serialized = SearchSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_images(request):
    instances = GiftImage.objects.filter(is_deleted=False)
    serialized = ImageSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)