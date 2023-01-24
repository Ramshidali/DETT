import json
from api.v1.general.functions import generate_serializer_errors
from api.v1.promotions.serializers import *
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import (get_object_or_404, )
from general.functions import get_auto_id
from products.models import ProductVariant, ProductCategory
from promotions.models import Enquiry
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_products(request):
    instances = ProductVariant.objects.filter(is_deleted=False, is_default=True)
    serialized = PVSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def product(request, pk):
    if ProductVariant.objects.filter(pk=pk):
        instances = ProductVariant.objects.get(pk=pk)
        seralized = PVSerializer(instances, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": seralized.data,
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": "Not found"
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def submit_enquiry(request):
    serialized = EnquirySerializer(data=request.data)
    if serialized.is_valid():
        auto_id = get_auto_id(Enquiry)
        enquiry_id = f"{str(auto_id).zfill(4)}"

        serialized.save(
            auto_id=auto_id,
            enquiry_id=enquiry_id,
        )

        response_data = {
            "StatusCode": 6000,
            "data": serialized.data
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": generate_serializer_errors(serialized._errors)
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_enquiries(request,phone):
    instances = Enquiry.objects.filter(is_deleted=False,enquirer_phone=phone)
    serialized = EnquiryViewSerializer(instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_enquiry(request, pk):
    if Enquiry.objects.filter(pk=pk):
        instances = Enquiry.objects.get(pk=pk)
        seralized = EnquiryViewSerializer(instances, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": seralized.data,
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": "Not found"
        }

    return Response(response_data, status=status.HTTP_200_OK)