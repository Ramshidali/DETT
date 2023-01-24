import datetime

from api.v1.general.functions import generate_serializer_errors, get_user
from api.v1.orders.product import ProductVariantDetails
from api.v1.orders.serializers import OrderSerializer, OrderTrackSerializer, \
    ProductVariantSerializer, OrderNotificationSerializer, \
    GetOrderSerializer
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from orders.models import Order, OrderItem, OrderStatus, OrderReview
from orders.orders import OrderManager
from products.models import ProductVariant
from reports.utils.invoice_manager import InvoiceManager
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from weasyprint import HTML


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_orders(request):
    """
    get all orders ordered by the customer
    :param request:
    :return:
    """
    order_instances = None
    query = request.GET.get('q')
    customer = get_user(request.user)
    order_item_instances = Order.objects.filter(customer=customer).order_by('-date_added')
    # order_item_instances = OrderItem.objects.filter(order__customer=customer)

    # orders count for checking on frontend
    orders_count = 0
    orders_count = OrderItem.objects.filter(order__customer=customer).count()

    if query:
        orders_count = OrderItem.objects.filter(order__customer=customer,
                                                product_variant__title__icontains=query).count()

    serialized = GetOrderSerializer(order_item_instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "orders": orders_count, "data": serialized.data, }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def place_order(request):
    """
    places the order based on cart added items
    :param request:
    :return: order response
    """

    # tomorrow updates
    # invoice fields values needed to be added
    response_data = {}
    try:
        serialized = OrderSerializer(data=request.data)
        order_manager = OrderManager()

        if serialized.is_valid():
            order = order_manager.place_order(order_serialized=serialized, request=request)
            is_item_order_saved = order_manager.save_order_items(request.user, order)

            if is_item_order_saved:
                response_data = {
                    "StatusCode": 6000,
                    "message": "Order placed",
                    "order_id": order.invoice_id
                }

            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": "Could not place order"
                }

        else:
            response_data = {
                "StatusCode": 6001,
                "message": generate_serializer_errors(serialized)
            }

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": "Please try again later!",
            "error": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def view_single_order_product(request, pk):
    """
    :param request:
    :return:
    """
    response_data = {}
    try:

        qty = request.GET.get('qty')

        product_variant = ProductVariantDetails(pk)
        variant_instance = product_variant.get_product_variant()
        amounts = product_variant.get_single_order_amounts(qty, request.user)

        print(amounts)

        serialized = ProductVariantSerializer(variant_instance, context={"request": request})

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "error": str(e),
            "message": "Please try again later"
        }
    else:
        response_data = {
            "StatusCode": 6000,
            "product_data": serialized.data,
            "totals": amounts,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def single_order_product_update_qty(request, pk):
    """
    api for single order product for updating qty
    :param request:
    :return:
    """
    response_data = {}
    try:
        qty = request.GET.get('qty')

        print("qtyy in request data", qty)

        product_variant = ProductVariantDetails(pk)
        variant_instance = product_variant.get_product_variant()
        amounts = product_variant.get_single_order_amounts(qty, request.user)

        serialized = ProductVariantSerializer(variant_instance, context={"request": request})

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "error": str(e),
            "message": "Please try again later"
        }
    else:
        response_data = {
            "StatusCode": 6000,
            "product_data": serialized.data,
            "totals": amounts,
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def place_single_order(request):
    """
    single product quick buying without adding to cart
    :param request:
    :return:
    """

    try:
        product_variant = request.data['product_variant']
        qty = request.data['qty']

        serialized = OrderSerializer(data=request.data)

        product_variant_details = ProductVariantDetails(product_variant)

        if serialized.is_valid():
            # if order placed successfully it returns True
            is_ordered = product_variant_details.place_single_order(request=request, serialized_value=serialized)

            if is_ordered:
                response_data = {"StatusCode": 6000, "data": serialized.data}

            else:
                response_data = {"StatusCode": 6001, "message": "Couldn't place order"}

        else:
            response_data = {"StatusCode": 6001, "message": generate_serializer_errors(serialized._errors)}

    except Exception as e:
        response_data = {
            "StatusCode": 6001, "message": "Please try again later !", "error": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_single_order(request, pk):
    """
    get single ordered product details,
    => shows order address
    => shows order items
    => totals
    :param request:
    :param pk:
    :return:
    """
    response_data = {}
    try:

        order_manager = OrderManager(pk)
        ordered_address = order_manager.get_order_address()
        ordered_items = order_manager.get_ordered_items(request)
        ordered_total = order_manager.get_orderd_totals()
        invoice_id = order_manager.get_invoice_id()

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "error": str(e),
            "message": "Please try again later"
        }
    else:
        response_data = {
            "StatusCode": 6000,
            "address": ordered_address,
            "ordered_items": ordered_items,
            "ordered_totals": ordered_total,
            "invoice_id": invoice_id,
        }

    # serialized = OrderWithAddressSerializer(instances, many=True, context={"request": request})

    # response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def track_order(request, pk):
    """
    order tracking functions
    :param request:
    :param pk:
    :return:
    """
    instances = Order.objects.get(pk=pk)
    serialized = OrderTrackSerializer(instances, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def cancel_order(request, pk):
    """
    order cancellation
    => update order status model and order model
    :param request:
    :param pk:
    :return:
    """
    Order.objects.filter(pk=pk).update(order_status=0)
    order_instance = Order.objects.get(pk=pk)
    date = datetime.date.today()
    order_instance.date_updated = datetime.date.today()
    order_instance.save()

    OrderStatus.objects.create(order=order_instance, status='0', date=date)

    response_data = {"StatusCode": 6000, "data": "Order Cancelled"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def rate_order(request, pk):
    """
    rate the order, pass the rating count
    :param request:
    :param pk:
    :return:
    """
    data = request.data
    star = data['star']

    instances = Order.objects.get(pk=pk)

    if OrderReview.objects.filter(order=pk).exists():
        OrderReview.objects.filter(order=pk).update(star=star)
    else:
        OrderReview.objects.create(order=instances, star=star)

    response_data = {"StatusCode": 6000, "data": str(star)}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def download_invoice(request, pk):
    """
    download order invoice
    :param request:
    :param pk:
    :return:
    """
    url = request.META['HTTP_HOST']
    scheme = request.scheme

    path = settings.MEDIA_ROOT
    file = f"/invoice_{pk}.pdf"

    template_path = 'pdf/invoice.html'

    order = Order.objects.get(pk=pk)

    order_manager = OrderManager(pk)
    ordered_items = order_manager.get_order_items_for_invoice()
    order_address = order_manager.get_order_address()
    order_total = order_manager.get_orderd_totals()
    order_details = order_manager.get_order_details()

    invoice_manager = InvoiceManager(order)
    invoice_totals = invoice_manager.get_invoice_totals()
    total_cgst = invoice_totals['gst_totals']['cgst']
    total_sgst = invoice_totals['gst_totals']['sgst']

    context = {
        "order_items": ordered_items,
        "order_address": order_address,
        "order_total": order_total,
        "order_details": order_details,
        "invoice_totals": invoice_totals,
        "total_cgst": total_cgst,
        "total_sgst": total_sgst
    }

    html_string = render_to_string(template_path, context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(f"{settings.MEDIA_ROOT}/invoices/invoice_{pk}.pdf")

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = f'filename=invoice_{pk}.pdf'

    response_data = {"StatusCode": 6000, "url": scheme + '://' + url + '/media/invoices' + file}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def order_notifications(request):
    customer = get_user(request.user)

    instances = OrderStatus.objects.filter(order__customer=customer).order_by('-date')
    serialized = OrderNotificationSerializer(instances, context={"request": request}, many=True)

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def check_product(request):
    product = request.GET.get('product')
    brand = request.GET.get('brand')
    variant = request.GET.get('variant')

    if ProductVariant.objects.filter(unit=variant, brand=brand, product=product).exists():
        response_data = {"StatusCode": 6000, "data": True}

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {"StatusCode": 6001, "data": False}

        return Response(response_data, status=status.HTTP_200_OK)
