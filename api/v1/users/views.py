import datetime
import decimal
import json
from api.v1.general.functions import generate_serializer_errors, get_total_amount, get_user, get_delivery_fee, \
    get_special_discount
from api.v1.users.serializers import DueDaysSerializer, ProductVariantSerializer, AddToCartSerializer, CartSerializer, \
    ChangeQtySerializer, ChangeSizeSerializer, CouponSerializer, OccassionSerializer, VariantSerializer, \
    ProductOccassionSerializer, AddressSerializer, OccassionListSerializer, PersonTypeSerializer, MomentCardSerializer, \
    ProductVariantSearchSerializer, VariantSizeSerializer, GetCouponSerializer, SliderSerializer
from customers.models import CustomerAddress, Customer, MomentCard
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import (get_object_or_404, )
from django.shortcuts import (get_object_or_404, )
from general.functions import get_auto_id
from general.models import SetDueDays, SetCoupon, PersonType, Slider
from products.models import ProductVariant, ProductForOccassion, Occassion, UnitOfMeasurement, Unit
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from users.models import ShoppingBagItem
from orders.models import CouponStatus


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def dashboard(request):
    """
    for showing the occasions and sub occasions
    :param request:
    :return:
    """
    instances = Occassion.objects.filter(is_deleted=False)
    serialized = OccassionSerializer(instances, many=True, context={"request": request})
    response_data = {"StatusCode": 6000, "data": serialized.data, }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_due_days(request):
    """
    function for getting due days, which means a it is a day only select a date after given due days
    :param request:
    :return:
    """
    instances = SetDueDays.objects.filter(is_deleted=False).first()
    serialized = DueDaysSerializer(instances, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data, }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def filter_gifts(request):
    """
    filter the gifts according to the given params, it is the screen coming after selecting due days
    :param request:
    :return: product variants
    """
    response_data = {}
    try:
        instances = []
        occassion_date = request.GET.get('occassion_date')
        person_name = request.GET.get('person_name')
        gender = request.GET.get('gender')
        age_group = request.GET.get('age_group')

        q = request.GET.get('q')
        size = request.GET.get('s')
        color = request.GET.get('c')
        brand = request.GET.get('b')
        try:
            brand = json.loads(brand)
        except:
            brand = None
        try:
            size = json.loads(size)
        except:
            size = None
        # print(size,type(size),"------------------------size")
        try:
            color = json.loads(color)
        except:
            color = None
        cat = request.GET.get('cat')
        try:
            cat = json.loads(cat)
        except:
            cat = None
        p = request.GET.get('p')
        try:
            p = json.loads(p)
        except:
            p = None

        instances = ProductVariant.objects.filter(gender=gender, age_group=age_group, is_default=True)
        # print(instances)

        if q == 'price_decrease':
            instances = ProductVariant.objects.filter(gender=gender, age_group=age_group, is_default=True).order_by(
                '-mrp')

        if q == 'price_increase':
            instances = ProductVariant.objects.filter(gender=gender, age_group=age_group, is_default=True).order_by(
                'mrp')

        if color:
            # print("color+++++++++++++++++")
            instances = instances.filter(color__in=color)

        if brand:
            instances = instances.filter(brand__in=brand)

        if size:
            instances = instances.filter(unit__in=size)

        if cat:
            instances = instances.filter(product__product_category__in=cat)

        if p == 'p1':
            instances = instances.filter(mrp__lte=249)

        if p == 'p2':
            instances = instances.filter(mrp__gte=250, mrp__lte=499)

        if p == 'p3':
            instances = instances.filter(mrp__gte=500, mrp__lte=999)

        if p == 'p4':
            instances = instances.filter(mrp__gte=1000, mrp__lte=1499)

        if p == 'p5':
            instances = instances.filter(mrp__gte=1500, mrp__lte=1999)

        if p == 'p6':
            instances = instances.filter(mrp__gte=2000, mrp__lte=2499)

        if p == 'p7':
            instances = instances.filter(mrp__gte=2500)

    except Exception as e:
        response_data = {"StatusCode": 6001, "message": "Please try again later", "error": str(e), }

    else:
        serialized = VariantSerializer(instances, many=True, context={"request": request})
        response_data = {"StatusCode": 6000, "data": serialized.data, }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def occassion_single_product(request, pk):
    instances = ProductForOccassion.objects.filter(occassion=pk, is_deleted=False)
    serialized = ProductOccassionSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def product(request, pk):
    """
    product single view functions
    :param request:
    :param product_variant pk:
    :return: product variant details
    """
    cart_instance = None
    instances = None
    customer = get_user(request.user)

    # check if product exists in cart
    if ShoppingBagItem.objects.filter(product_variant=pk, customer=customer).exists():
        cart_instance = ShoppingBagItem.objects.filter(product_variant=pk, customer=customer)

    if ProductVariant.objects.filter(pk=pk):
        instances = ProductVariant.objects.get(pk=pk)

    if instances:
        seralized = ProductVariantSerializer(instances, context={"request": request})
        if cart_instance:
            response_data = {"StatusCode": 6000, "data": seralized.data, "cart": True}
        else:
            response_data = {"StatusCode": 6000, "data": seralized.data, "cart": False}

    else:
        response_data = {"StatusCode": 6001, "data": "Product Not Found"}

    print(response_data)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def add_to_cart(request, pk):
    """'
    add to cart using product variant pk
    :param request:
    :param pk:
    """
    response_data = {}

    try:
        product_variant_instance = ProductVariant.objects.get(pk=pk)
        available_stock = product_variant_instance.stock

    except Exception as e:
        response_data = {"StatusCode": 6001, "message": "Please try again later", "error": str(e), }

    else:
        if available_stock > 0:
            if not ShoppingBagItem.objects.filter(product_variant=product_variant_instance,
                                              customer__user=request.user).exists():

                ShoppingBagItem.objects.create(product_variant=product_variant_instance, customer=get_user(request.user))

                response_data = {"StatusCode": 6000, "message": "Product Added to Cart"}

            else:
                response_data = {"StatusCode": 6001, "message": "Product already added to cart"}

        else:
            response_data = {"StatusCode": 6001, "message": "Out Of Stock"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def cart(request):
    """
    view cart page of the customer and consist of coupon code discount based calculations
    :param request:
    :return: cart objects
    """
    try:
        customer = get_user(request.user)

        response_data = {}

        special_discount_amt = 0
        is_coupon = False
        coupon = ""
        discounted_price = 0

        instances = ShoppingBagItem.objects.filter(customer=customer)

        serialized = CartSerializer(instances, many=True, context={"request": request})

        grand_total = 0

        # special_discount, igst, sgst, cgst, grand_total, item_total
        all_totals = get_total_amount(customer)

        grand_total = round(all_totals['grand_total'])
        item_total = decimal.Decimal(all_totals['item_total'])

        gst = (all_totals['cgst']) + (all_totals['sgst'])

        # check for applied coupons
        instance = None
        special_discount = 0
        discounted_price = 0

        if CouponStatus.objects.filter(customer=customer, is_applied=True, status=False, is_deleted=False).order_by(
                '-date_added').exists():
            instance = CouponStatus.objects.filter(customer__user=request.user, is_applied=True, status=False,
                                                   is_deleted=False).order_by('-date_added').first()
            is_coupon = True
            coupon = instance.coupon.coupon_code
            discount_percent = int(instance.coupon.offer_percentage)
            discounted_price = (grand_total * discount_percent) / 100

            grand_total = grand_total - discounted_price

            special_discount_amt = discount_percent

            print("discounted price==>>", discounted_price)
            print("Percent==>>", discount_percent)
            print("total amount ==>>", grand_total)

            response_data = {"StatusCode": 6000, "data": serialized.data, "item_total": all_totals['item_total'],
                             "special_discount_percent": special_discount_amt, "grand_total": grand_total,
                             "is_coupon": is_coupon,
                             "coupon_details": {
                                 "coupon": coupon,
                                 "coupon_pk": instance.coupon.pk,
                             },
                             "discounted_price": discounted_price, "gst": gst}
        else:
            response_data = {"StatusCode": 6000, "data": serialized.data, "item_total": all_totals['item_total'],
                         "special_discount_percent": special_discount_amt, "grand_total": grand_total, "is_coupon": is_coupon,
                          "discounted_price": discounted_price,"gst":gst}
    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "error": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_qty(request, pk):
    """
    change cart item quantity using cart item pk
    :param request:
    :param pk:
    :body_params: qty
    :return:
    """
    serialzed = ChangeQtySerializer(data=request.data)
    response_data = {}

    instances = None
    if ShoppingBagItem.objects.filter(pk=pk, is_deleted=False).exists():
        instances = ShoppingBagItem.objects.get(pk=pk, is_deleted=False)

    if instances:
        if serialzed.is_valid():
            serialzed.update(instances, serialzed.data)

            response_data = {"StatusCode": 6000, "message": "Quantity Updated", "data": serialzed.data}

        else:
            response_data = {"StatusCode": 6001, "message": generate_serializer_errors(serialzed.errors)}

    else:
        response_data = {"StatusCode": 6001, "data": "Item not found"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_size(request, pk):
    """
    change product using product in the cart
    :param request:
    :param pk:
    :return: cart response
    """
    response_data = {}

    try:
        data = request.data
        product_variant_pk = data['product_variant_pk']

        product_variant_instance = ProductVariant.objects.get(pk=product_variant_pk)
        available_stock = product_variant_instance.stock

    except Exception as e:

        response_data = {"StatusCode": 6001, "message": "Please try again later", "error": str(e), }

    else:

        if available_stock > 0:
            if ShoppingBagItem.objects.filter(pk=pk).exists():

                old_cart_item_instance = ShoppingBagItem.objects.get(pk=pk)
                old_cart_item_instance.product_variant = product_variant_instance
                old_cart_item_instance.save()

                response_data = {"StatusCode": 6000, "message": "Product Added to Cart"}

            else:
                response_data = {"StatusCode": 6001, "message": "Cart item not found"}

        else:
            response_data = {"StatusCode": 6001, "message": "Out Of Stock"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def remove_item(request, pk):
    """
    remove a cart item instance using cart item pk
    :param request:
    :param pk:
    :return: cart response
    """

    instances = None
    if ShoppingBagItem.objects.filter(pk=pk):
        instances = ShoppingBagItem.objects.get(pk=pk)

    if instances:
        obj = get_object_or_404(ShoppingBagItem, pk=pk)
        obj.delete()
        response_data = {"StatusCode": 6000, "message": "Item removed"}

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "message": "No items found "}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def apply_coupon(request):
    """
    applying a specific coupon code
    :param request:
    :return: coupon status response
    """
    response_data = {}
    try:
        coupon = request.data.get('coupon_code')

        instances = None
        response_data = {}

        if SetCoupon.objects.filter(coupon_code=coupon, is_deleted=False):
            instances = SetCoupon.objects.get(coupon_code=coupon, is_deleted=False)
    except Exception as e:
        response_data = {"StatusCode": 6001, "message": "Please try again later", "error": str(e), }
    else:

        if instances:
            # check is coupon applied
            if CouponStatus.objects.filter(coupon__coupon_code=coupon, customer__user=request.user,
                                           is_applied=True,status=True).exists():
                response_data = {"StatusCode": 6001, "data": "Coupon is already applied"}

            else:
                # coupon apllying
                data = CouponStatus.objects.create(customer=get_user(request.user), is_applied=True, coupon=instances)
                response_data = {"StatusCode": 6000, "data": "Coupon applied sucessfully"}
        else:
            response_data = {"StatusCode": 6001, "message": "Invalid Coupon Code"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def cancel_coupon(request, pk):
    """
    mark the applied coupon as is_deleted and is_applied False
    :param request:
    :body_params: coupon_code
    :return: coupon status
    """
    response_data = {}
    try:
        coupon_instance = CouponStatus.objects.filter(coupon__pk=pk, is_deleted=False, is_applied=True, status=False,
                                        customer__user=request.user).first()

    except Exception as e:
        response_data = {"StatusCode": 6001, "message": "Please try again later !", "error": str(e), }

    else:
        coupon_instance.is_applied = False
        coupon_instance.is_deleted = True
        coupon_instance.save()

        response_data = {"StatusCode": 6000, "data": "Coupon Cancelled sucessfully"}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_coupons(request):
    """
    for fetching all coupons
    :param request:
    :return: coupon objects
    """
    instances = SetCoupon.objects.filter(is_deleted=False)

    q = request.GET.get('q')
    if q:
        instances = instances.filter(coupon_code__icontains=q)

    serialized = GetCouponSerializer(instances, many=True)

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def add_address(request):
    """
    function for adding authenticated customer addresses
    :param request:
    :body_params: name, address_line1, phone, pincode, street, city, landmark, city, is_default, address_type
    :return:

    """
    serialized = AddressSerializer(data=request.data)
    is_default = None
    if serialized.is_valid():
        isTrue = serialized.validated_data['is_default']
        customer = request.user
        user = Customer.objects.get(phone=customer)
        is_default = CustomerAddress.objects.filter(customer=user, is_deleted=False)

        if is_default and isTrue == True:
            CustomerAddress.objects.filter(customer=user, is_deleted=False).update(is_default=False)
        serialized.save(customer=user)
        response_data = {"StatusCode": 6000, "message": serialized.data, }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "message": generate_serializer_errors(serialized._errors)}

        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_address(request, pk):
    """
    Edit the added added by the user
    :param request:
    :param pk:
    :return: edited address object
    """
    instances = None
    name = request.data['name']
    address_line1 = request.data['address_line1']
    phone = request.data['phone']
    pincode = request.data['pincode']
    street = request.data['street']
    city = request.data['city']
    landmark = request.data['landmark']
    state = request.data['state']
    address_type = request.data['address_type']
    

    if CustomerAddress.objects.filter(pk=pk).exists():
        instances = CustomerAddress.objects.get(pk=pk)

    if instances:
        CustomerAddress.objects.filter(pk=pk).update(name=name, address_line1=address_line1, phone=phone, 
                                                     pincode=pincode, street=street, city=city, landmark=landmark,
                                                     state=state, address_type=address_type)
        response_data = {"StatusCode": 6000, "data": "Successfully Changed"}

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "data": "Not found"}

        return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def view_address(request):
    """
    view all the created addresses
    :param request:
    :return:
    """
    user = get_user(request.user)
    instances = CustomerAddress.objects.filter(customer=user, is_deleted=False)
    serialized = AddressSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def delete_address(request, pk):
    """
    mark the address object as deleted
    :param request:
    :param pk:
    :return: deleted response
    """
    if CustomerAddress.objects.filter(pk=pk, is_deleted=False).exists():
        CustomerAddress.objects.filter(pk=pk).update(is_deleted=True)
        response_data = {"StatusCode": 6000, "message": "Data deleted Sucessfully"}
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "message": "Address not found"}

        return Response(response_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def occassions(request):
    instances = Occassion.objects.filter(is_deleted=False)
    serialized = OccassionListSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def occassions(request):
    """
    listing for all the occasions
    :param request:
    :return: occasion objects
    """
    instances = Occassion.objects.filter(is_deleted=False)
    serialized = OccassionListSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def person_types(request):
    """
    for listing person types
    :param request:
    :return: person type objects
    """
    instances = PersonType.objects.filter(is_deleted=False)
    serialized = PersonTypeSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_moment_card(request):
    """
    creation of moment card, added by the user
    :param request:
    :return: moments card resposne
    """
    serialized = MomentCardSerializer(data=request.data)
    if serialized.is_valid():
        user = get_user(request.user)
        serialized.save(customer=user)

        response_data = {"StatusCode": 6000, "message": serialized.data, }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "message": generate_serializer_errors(serialized._errors)}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def moment_cards(request):
    """
    The listing of moment card added by the user
    :param request:
    :return: moments cards objects
    """
    user = get_user(request.user)
    instances = MomentCard.objects.filter(is_deleted=False, customer=user)
    serialized = MomentCardSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_moment_card(request, pk):
    """
    Edit the momemt cards added by the user
    :param request:
    :param pk:
    :return: edited moment card object
    """
    instances = None
    person_type = request.data['person_type']
    person_name = request.data['person_name']
    occassion = request.data['occassion']
    event_date = request.data['event_date']
    meta = request.data['meta']
    title = request.data['title']
    customer = get_user(request.user)

    person_type_instances = PersonType.objects.get(pk=person_type)
    occassion_instances = Occassion.objects.get(pk=occassion)

    if MomentCard.objects.filter(pk=pk).exists():
        instances = MomentCard.objects.get(pk=pk)

    if instances:
        MomentCard.objects.filter(pk=pk).update(title=title, occassion=occassion_instances,
                                                person_type=person_type_instances, person_name=person_name,
                                                event_date=event_date, meta=meta, )
        response_data = {"StatusCode": 6000, "data": "Successfully Changed"}

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "data": "Not found"}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def delete_moment_card(request, pk):
    """
    mark the moments card object as deleted
    :param request:
    :param pk:
    :return: deleted response
    """
    if MomentCard.objects.filter(pk=pk, is_deleted=False).exists():
        MomentCard.objects.filter(pk=pk).update(is_deleted=True)
        response_data = {"StatusCode": 6000, "message": "Data deleted Sucessfully"}
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "message": "Moment card instance not found"}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def view_default_address(request):
    """
    function for view the current default selected address
    :param request:
    :return: The one default selected address
    """
    user = get_user(request.user)
    instances = None
    if CustomerAddress.objects.filter(is_default=True, customer=user, is_deleted=False).exists():
        instances = CustomerAddress.objects.get(is_default=True, customer=user, is_deleted=False)

    if instances:
        serialized = AddressSerializer(instances, context={"request": request})

        response_data = {"StatusCode": 6000, "data": serialized.data}
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        serialized = AddressSerializer(instances, context={"request": request})

        response_data = {"StatusCode": 6001, "data": "No default address found"}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def set_default_address(request, pk):
    """
    set a default address
    :param request:
    :param pk:
    :return: default address
    """
    user = get_user(request.user)

    instances = None
    if CustomerAddress.objects.filter(customer=user, is_deleted=False).exists():
        CustomerAddress.objects.filter(is_default=True, customer=user, is_deleted=False).update(is_default=False)
        instances = CustomerAddress.objects.filter(pk=pk).update(is_default=True)

    if instances:
        serialized = AddressSerializer(instances, context={"request": request})

        response_data = {"StatusCode": 6000, "message": "Updated Sucessfully"  # "data": serialized.data
                         }
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {"StatusCode": 6001, "data": "not found"}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def search_product(request):
    instances = ProductVariant.objects.filter(is_default=True, is_deleted=False)

    query = request.GET.get('q')
    if query:
        instances = instances.filter(title__icontains=query)

    serialized = ProductVariantSearchSerializer(instances, many=True, context={"request": request})

    response_data = {"StatusCode": 6000, "data": serialized.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_sizes(request, pk):
    """
    get the unit of measurements for product filtering
    :param request:
    :param pk:
    :return: unit of measurements
    """

    instances = UnitOfMeasurement.objects.filter(is_deleted=False)
    serialised = VariantSizeSerializer(instances, many=True)

    response_data = {"StatusCode": 6000, "message": serialised.data}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def sliders(request):
    """
    home screen sliders
    :param request:
    :return: sliders response
    """
    instances = Slider.objects.filter(is_deleted=False)
    serialised = SliderSerializer(instances, many=True, context={"request": request})
    response_data = {"StatusCode": 6000, "message": serialised.data}

    return Response(response_data, status=status.HTTP_200_OK)
