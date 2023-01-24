import json
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.template.context_processors import csrf
from django.urls import reverse
from api.v1.orders.serializers import GetOrderSerializer
from general.utils.sms import SMS

import razorpay
from general.functions import get_auto_id, get_otp, decrypt_message, encrypt_message, send_email, send_sms
from customers.models import Customer, CustomerAddress, Otp
from orders.models import Order, OrderItem, OrderStatus
from products.models import Product, ProductCategory, ProductImage, ProductVariant
from web.forms import CustomerAddressForm
from web.serializers import AddressSerializers

client = razorpay.Client(
    auth=("rzp_test_lXb6SxVILCvIy6", "R4A7PV1MQxgHXKKpeyjGogji"))


def index(request):

    context = {
        "title": "Dett",
        "is_users": True,
        "is_home": True,
    }

    return render(request, 'web/index.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('web:index', ))


def otp_generation(request):
    name = request.GET.get("fname")
    phone = request.GET.get("phone")
    # print("hi")
    otp = get_otp()

    response_data = {}

    if phone:
        # print("phone")
        if len(phone) == 10:
            # print("phone length")

            if Otp.objects.filter(phone=phone).exists():
                # print("exist otp")
                Otp.objects.filter(phone=phone).update(
                    otp=str(otp),
                )

                message = f"Dear customer, {otp} is your OTP from DETT. Don't share your OTP with anyone."
                # msg = sendSMS('otp', phone, [otp])
                # print('\n\n-------------', msg, '-------------\n\n')

                # print(message)
                sms_manager = SMS(phone)
                sms_manager.send_otp(otp)

                response_data = {
                    "status": "true",
                    "name": name,
                    "phone": phone,
                }

            else:
                message = f"Dear customer, {otp} is your OTP from DETT. Don't share your OTP with anyone."
                # msg = sendSMS('otp', phone, [otp])
                # print('\n\n-------------', msg, '-------------\n\n')

                # print(message)

                otp_data = Otp.objects.create(
                    phone=phone,
                    otp=otp,
                )
                sms_manager = SMS(phone)
                sms_manager.send_otp(otp)

                response_data = {
                    "status": "true",
                    "name": name,
                    "phone": phone,
                }

        else:
            response_data = {
                "status": 'number_not_valid',
                "message": "Please enter your 10 digit mobile number without space and don't add 91 or 0 or +91 before your number"
            }

    else:
        # print("phone number not found")
        response_data = {
            "status": "6001"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def verify_otp(request):
    response_data = {}

    name = request.GET.get("fname")
    phone = request.GET.get("phone")
    # print(name)
    # print(phone)

    otp_one = request.GET.get("otp_one")
    otp_two = request.GET.get("otp_two")
    otp_three = request.GET.get("otp_three")
    otp_four = request.GET.get("otp_four")

    otp_final = otp_one + otp_two + otp_three + otp_four

    # print(phone, otp_final,"---otp_final")

    if otp_final:
        # print("2222222222")
        if Otp.objects.filter(phone=phone).exists():
            # print("3333333")
            if Otp.objects.filter(phone=phone, otp=otp_final).exists():
                # print("44")
                otp_show = Otp.objects.get(phone=phone)

                if User.objects.filter(username=phone).exists() and not Customer.objects.filter(user=phone).exists():
                    user = User.objects.filter(username=phone)
                    user.delete()

                if not Customer.objects.filter(phone=phone).exists():
                    user_data = User.objects.create_user(
                        username=phone, password=phone, is_active=True,)

                    group, created = Group.objects.get_or_create(
                        name="customer_user")
                    user_data.groups.add(group)
                    user_data.save()

                    Customer.objects.create(
                        auto_id=get_auto_id(Customer),
                        user=user_data,
                        creator=user_data,
                        updater=user_data,
                        name=name,
                        phone=phone,
                        otp=otp_final,
                        password=encrypt_message(phone)
                    )
                # print(phone,"++++++++++=========")
                user = authenticate(username=phone, password=phone)
                if user is not None:
                    # print("userrr")
                    login(request, user)
                # print("varify true")
                response_data = {
                    "status": "true",
                }
            else:
                # print("varify false")
                response_data = {
                    "status": "false",
                    "condition_status": "not_match",
                    "message": "otp not match please enter otp",
                }
        else:
            response_data = {
                "status": "phone number not exist"
            }

    else:
        # print("varify error")

        response_data = {
            "status": "false"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def gifts(request):
    categories = ProductCategory.objects.filter(is_deleted=False)
    instances = ProductVariant.objects.filter(
        is_deleted=False, is_default=True)

    query = request.GET.get("q")
    filter_data = {}

    if query:
        instances = instances.filter(
            Q(product__name__icontains=query)
        )
        filter_data['q'] = query

    category__pk = request.GET.get("category-id")

    if category__pk:
        instances = ProductVariant.objects.filter(
            is_deleted=False, is_default=True, product__product_category_id=category__pk)

    paginator = Paginator(instances, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Gifts",
        "instances": instances,
        "categories": categories,
        'filter_data': filter_data,
        'category__pk': category__pk,
        'page_obj': page_obj,

        "is_users": True,
        "is_gift": True,
    }

    return render(request, 'web/gift.html', context)


def terms(request):

    context = {
        "title": "terms",
        "is_terms": True,
    }

    return render(request, 'web/conditions.html', context)

def privacy(request):

    context = {
        "title": "privacy",
        "is_privacy": True,
    }

    return render(request, 'web/conditions.html', context)


def return_policy(request):

    context = {
        "title": "return",
        "is_return": True,
    }

    return render(request, 'web/conditions.html', context)

def delivery(request):

    context = {
        "title": "delivery",
        "is_delivery": True,
    }

    return render(request, 'web/conditions.html', context)


def product(request, pk):
    instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
    units = ProductVariant.objects.filter(product=instance.product)

    product_image = ProductImage.objects.filter(
        product_variant=instance, is_deleted=False)

    offer = (instance.mrp-instance.price) / instance.mrp
    offer_rate = offer * 100

    context = {
        "instance": instance,
        "title": "Product",
        "is_users": True,
        "offer_rate": offer_rate,
        "units": units,
        "product_image": product_image,
    }

    return render(request, 'web/product.html', context)


def buy_now_address(request, pk):
    if request.user.is_authenticated and not request.user.is_superuser:

        instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
        address = CustomerAddress.objects.filter(
            customer__user=request.user, is_deleted=False).order_by("id")

        address_form = CustomerAddressForm()

        context = {
            "instance": instance,
            "address": address,
            "address_form": address_form,
            "title": "Address",
            "is_users": True,
            "is_addressform": True,
        }

        return render(request, 'web/buyNowAddress.html', context)

    else:

        return HttpResponseRedirect(reverse('web:index', ))


def buy_now_address_next(request, pk):
    if request.user.is_authenticated and not request.user.is_superuser:

        instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
        units = ProductVariant.objects.filter(product=instance.product)
        address = CustomerAddress.objects.get(
            customer__user=request.user, is_default=True, is_deleted=False)

        offer = (instance.mrp-instance.price) / instance.mrp
        offer_rate = offer * 100
        # print(instance.stock, "=======================")
        # stocks = list(map(int, str(instance.stock) if instance.stock > 1 else "0"))

        context = {
            "instance": instance,
            "units": units,
            "address": address,
            "offer_rate": offer_rate,
            "title": "Address",
            "is_users": True,
            # "stocks" : stocks,
        }

        return render(request, 'web/buynowaddresssingle.html', context)

    else:

        return HttpResponseRedirect(reverse('web:index', ))


def buy_now_add_address(request, pk):
    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:

        if request.method == 'POST':
            form = CustomerAddressForm(request.POST)
            address_type = request.POST.get('address_type')
            customer = Customer.objects.get(
                user=request.user, is_deleted=False)
            CustomerAddress.objects.filter(
                customer=customer, is_deleted=False).update(is_default=False)

            if form.is_valid():
                # print("valid")
                data = form.save(commit=False)
                data.date_added = datetime.today()
                data.customer = customer
                data.address_type = address_type
                data.is_default = True
                data.save()

                if pk == "":
                    return HttpResponseRedirect(reverse("web:profile"))
                else:
                    return HttpResponseRedirect(reverse("web:buy_now_address", kwargs={'pk': pk}))

            else:
                print("not valid")
                if pk == "":
                    response_data = {
                        "status": "false",
                        "title": "Failed",
                        "message": "Form validation error",
                        "redirect_url": reverse("web:buy_now_address", kwargs={'pk': pk})
                    }
                else:
                    response_data = {
                        "status": "false",
                        "title": "Failed",
                        "message": "Form validation error",
                        "redirect_url": reverse("web:profile")
                    }

                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            if pk == "":
                response_data = {
                    "status": "true",
                    "title": "Failed",
                    "message": "Not POST",
                    "redirect_url": reverse("web:buy_now_address", kwargs={'pk': pk})
                }
            else:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Form validation error",
                    "redirect_url": reverse("web:profile")
                }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        return HttpResponseRedirect(reverse('web:index', ))

# get value from db into ajax


def edit_address(request, pk):
    response_data = {}
    if request.user.is_authenticated and not request.user.is_superuser:

        address = CustomerAddress.objects.get(
            pk=pk, customer__user=request.user)
        serialized = AddressSerializers(address, context={"request": request})

        response_data = {
            "status": "true",
            "data": serialized.data,
        }
    else:
        response_data = {
            "status": "false",
            "title": "Failed",
            "message": "no user",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def update_address(request, pk):
    response_data = {}
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == 'POST':
            instance = CustomerAddress.objects.get(
                pk=pk, customer__user=request.user)
            form = CustomerAddressForm(request.POST, instance=instance)
            address_type = request.POST.get('address_type')
            CustomerAddress.objects.filter(
                customer__user=request.user, is_deleted=False).update(is_default=False)

            if form.is_valid():
                data = form.save(commit=False)
                data.address_type = address_type
                data.is_default = True
                data.save()

                return HttpResponseRedirect(reverse("web:profile"))
            else:
                print("not valid")
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Form validation error",
                    "redirect_url": reverse("web:profile")
                }

                return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        return HttpResponseRedirect(reverse('web:profile', ))
    else:
        return HttpResponseRedirect(reverse('web:index', ))


def set_default_address(request, pk):
    # print(pk)
    if request.user.is_authenticated and not request.user.is_superuser:

        CustomerAddress.objects.filter(
            is_deleted=False).update(is_default=False)
        CustomerAddress.objects.filter(
            pk=pk, is_deleted=False).update(is_default=True)

        response_data = {
            "status": "true",
            "title": "successfull",
            "message": "address successfully completed",
        }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        return HttpResponseRedirect(reverse('web:index', ))


def profile(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        profile_instance = Customer.objects.get(
            user=request.user, is_deleted=False)
        profile_address = CustomerAddress.objects.filter(
            customer=profile_instance, is_deleted=False)

        if OrderItem.objects.filter(order__customer=profile_instance, order__is_deleted=False).exists():
            my_orders = OrderItem.objects.filter(
                order__customer=profile_instance, order__is_deleted=False).order_by("-order__date_added")
        else:
            my_orders = OrderItem.objects.none()

        address_form = CustomerAddressForm()

        context = {
            "profile_instance": profile_instance,
            "profile_address": profile_address,
            "address_form": address_form,
            "my_orders": my_orders,
            "is_profile": True,
            "is_addressform": True,
            'page_name': 'Profile',
        }

        return render(request, 'web/profile.html', context)

    else:

        return HttpResponseRedirect(reverse('web:index', ))


def place_order(request, pk):
    if request.user.is_authenticated and not request.user.is_superuser:

        instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
        customer = Customer.objects.get(user=request.user, is_deleted=False)
        billing_address = CustomerAddress.objects.get(
            customer__user=request.user, is_default=True, is_deleted=False)

        name = billing_address.name
        city = billing_address.city
        state = billing_address.state
        phone = billing_address.phone
        street = billing_address.street
        pincode = billing_address.pincode
        landmark = billing_address.landmark
        address = billing_address.address_line1

        # totola price calculation
        total_cgst = 0
        total_sgst = 0
        total_igst = 0
        gst_total = 0
        total_amount = 0

        cgst = instance.product.gst_code.cgst_rate / 100
        sgst = instance.product.gst_code.sgst_rate / 100
        igst = instance.product.gst_code.igst_rate / 100

        # appended to the totals gst fields
        total_cgst = total_cgst + cgst
        total_sgst = total_sgst + sgst
        total_igst = total_igst + igst

        # total igst removed needed to be added
        gst_total += total_cgst + total_sgst
        total_amount = gst_total + instance.price

        auto_id = get_auto_id(Order)
        invoice_id = f"DT2223/{str(auto_id).zfill(4)}"
        # print(auto_id,"auto======")

        order_data = Order.objects.create(
            auto_id=auto_id,
            creator=request.user,
            updater=request.user,

            customer=customer,
            billing_name=name,
            billing_phone=phone,
            billing_address=address,
            billing_city=city,
            billing_state=state,
            pincode=pincode,
            total_amt=total_amount,
            payment_method="upi",
            invoice_id=invoice_id,
        )

        order_item = OrderItem.objects.create(
            product_variant=instance,
            price=instance.price,
            order=order_data,
        )

        order_status = OrderStatus.objects.create(
            status="10",
            order=order_data,
        )

        message = f"Dear DETT customer, your order {order_data} is placed and expected delivery by 10 days "
        if not customer.email is None:
            # print(customer.email,"email;;========")
            send_email("Dett Order Status", customer.email, message)
        # ('\n\n-------------', msg, '-------------\n\n')
        # print(phone)
        # sms_manager = SMS(phone)
        # sms_manager.gift_packed(order_data.invoice_id)

        return HttpResponseRedirect(reverse('web:payment_gateway', kwargs={'order_id': order_data.pk}))

    else:

        return HttpResponseRedirect(reverse('web:index', ))


@csrf_protect
@csrf_exempt
def payment_gateway(request, order_id):
    if Order.objects.filter(pk=order_id, is_deleted=False).exists():
        order_instance = Order.objects.get(pk=order_id, is_deleted=False)

        order_currency = 'INR'
        order_receipt = order_id
        order_amount = order_instance.total_amt
        name = order_instance.customer.name
        email = order_instance.customer.email
        notes = {'Shipping address': order_instance.billing_address}

        total_amount = order_amount * 100

        response = client.order.create(dict(amount=int(float(
            total_amount)), currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        payment_order_id = response['id']
        Order.objects.filter(pk=order_id, is_deleted=False).update(
            payment_order_id=payment_order_id)

    context = {
        "payment_order_id": order_instance.pk,
        "payment_order_id": payment_order_id,
        "order_amount": str(order_amount),
        "current_amount": str(order_amount),
        "name": name,
        "email": email,
        "notes": notes,
        "redirect_url": reverse('web:payment_response', kwargs={'order_id': order_id}),

        'page_name': 'Payment Page',
        'page_title': 'Payment Page',

    }

    return render(request, 'web/payment_page.html', context)


#=====================================payment section starting============================#
@csrf_protect
@csrf_exempt
@require_POST
def payment_response(request, order_id):
    # print("payment response")
    response = request.POST

    c = {}
    c.update(csrf(request))

    params_dict = {
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    order = Order.objects.filter(pk=order_id, is_deleted=False)
    # print(order,"------order----------")
    status = client.utility.verify_payment_signature(params_dict)
    # print(status,"status------------------------")
    if status == False:
        order.payment_status = "failed"
        order.save()

        return render(request, 'web/order_summary.html', {'status': 'Payment Faliure!!!'})
        # return HttpResponseRedirect(reverse("web:payment_failed"))

    else:
        # print("else")
        order.update(
            transaction_id=params_dict['razorpay_payment_id'],
            order_status="10",
        )
        order_item = OrderItem.objects.get(order__pk=order_id)
        product_varient = ProductVariant.objects.get(
            pk=order_item.product_variant.pk)

        product_varient.stock -= 1
        product_varient.save()

        success = "yes"
        message = "Success! Your transaction has been successfully processed."

        return HttpResponseRedirect(reverse("web:payment_success", kwargs={'order_id': order_id}))


def payment_success(request, order_id):
    orders = OrderItem.objects.filter(order__pk=order_id, is_deleted=False)
    address = Order.objects.get(pk=order_id, is_deleted=False)

    context = {
        "orders": orders,
        "address": address,
        "title": "Payment Success",
    }

    return render(request, 'web/payment_success.html', context)


#===========================================payment section end================================#
