import datetime
import decimal
import random
import re
import string

import requests
from customers.models import Customer
from customers.models import CustomerAddress
from general.models import Extras
from orders.models import CouponStatus
from orders.models import OrderItem, Order
from products.models import ProductVariant
from users.models import ShoppingBagItem


def generate_serializer_errors(args):
    message = ''
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += "%s : %s |" % (key, error_message)
    return message[:-3]


def get_user_token(request, user_name, password):
    headers = {'Content-Type': 'application/json', }
    data = '{"username": "' + user_name + '", "password":"' + password + '"}'
    print(data, "--data")
    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    web_host = request.get_host()
    request_url = protocol + web_host + "/api/v1/auth/token/"

    print(request_url, "--------request_url")

    response = requests.post(request_url, headers=headers, data=data)
    print(response, "------response2")
    return (response)


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def check_paswword_strength(password):
    if (len(password) >= 8):
        if (bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', password)) == True):
            return True
        elif (bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})', password)) == True):
            return "Password is weak"
    else:
        return "Password is weak"


def get_current_date():
    return datetime.date.today()


def get_total_amount(customer):
    """
    get all the totals including total_amt, discount, item_total etc.
    :param customer:
    :return:
    """
    response_data = {}

    try:
        instances = ShoppingBagItem.objects.filter(customer=customer)

        amt = 0
        total_cgst = 0
        total_sgst = 0
        total_igst = 0

        # take the special discount
        extras = Extras.objects.get(id=1)
        special_discount = extras.special_discount

        grand_total = 0
        item_total = 0
        discount = 0

        print("Beforre for looop")

        for i in instances:
            # calculating the gst codes
            amt = i.product_variant.price * i.qty
            cgst = 0
            sgst = 0
            igst = 0
            print(type(amt))
            if i.product_variant.product.gst_code.cgst_rate != 0:
                print("------------------",i.product_variant.product.gst_code.cgst_rate)
                cgst = amt  * i.product_variant.product.gst_code.cgst_rate / 100
                print('cgst----------',cgst)
                
            if i.product_variant.product.gst_code.sgst_rate != 0:
                sgst = amt  * i.product_variant.product.gst_code.sgst_rate / 100

            if i.product_variant.product.gst_code.igst_rate != 0:
                igst = amt  * i.product_variant.product.gst_code.igst_rate / 100

            print("Inside loop")

            # appended to the totals gst fields
            total_cgst = total_cgst + cgst
            total_sgst = total_sgst + sgst
            total_igst = total_igst + igst

            # total igst removed needed to be added
            grand_total += total_cgst + total_sgst + amt
            item_total += amt

            print("Trye last section")

    except Exception as e:
        print("error section")
        print(str(e))
        response_data = {"status": False, "error": str(e), }

    else:
        print("else section")
        response_data = {
            "status": True,
            "special_discount": special_discount,
            "igst": total_igst,
            "sgst": total_sgst,
            "cgst": total_cgst,
            "grand_total": grand_total,
            "item_total": item_total,
        }

    return response_data


def get_delivery_fee(customer):
    extras = Extras.objects.get(pk=1)

    inter_state_rate = extras.inter_state_charges
    intra_state_rate = extras.intra_state_charges
    special_discount = extras.special_discount

    delivery_fee = 0
    if CustomerAddress.objects.filter(customer=customer, is_default=True, is_deleted=False).exists():
        address = CustomerAddress.objects.get(customer=customer, is_deleted=False, is_default=True)
        if address.state == 'kerala' or address.state == 'Kerala' or address.state == 'KL':
            delivery_fee = int(intra_state_rate)
        else:
            delivery_fee = int(inter_state_rate)

    return delivery_fee


def get_special_discount():
    extras = Extras.objects.get(pk=1)
    special_discount = extras.special_discount

    return special_discount


def get_user(user):
    print("======>>><><>>", user)
    user = Customer.objects.get(phone=user)
    return user


def clear_cart(customer, order):
    instances = None
    if ShoppingBagItem.objects.filter(customer=customer):
        instances = ShoppingBagItem.objects.filter(customer=customer)
        for i in instances:
            OrderItem.objects.create(product_variant=i.product_variant, qty=i.qty, order=order,
                                     price=i.product_variant.price)

            product = ProductVariant.objects.get(id=i.product_variant.id)
            stock = product.stock
            if stock > 0:
                ProductVariant.objects.filter(id=i.product_variant.id).update(stock=stock - i.qty)
                i.delete()
            else:
                return False
        return True
    else:
        return False


def get_taxable_amt(items):
    total = 0
    for i in items:
        total = total + i.price

    return total


def get_cgst(items):
    cgst = 0
    for i in items:
        cgst = cgst + i.product_variant.product.hsn_code.cgst_rate

    return cgst


def get_sgst(items):
    sgst = 0
    for i in items:
        sgst = sgst + i.product_variant.product.hsn_code.sgst_rate

    return sgst


def is_kerala(user):
    user = get_user(user)

    if CustomerAddress.objects.filter(customer=user, is_deleted=False, is_default=True).exists():
        address = CustomerAddress.objects.get(customer=user, is_deleted=False, is_default=True)
        if address.state == 'kerala' or address.state == 'Kerala' or address.state == 'KL':
            print("hhh")
            return 1
        else:
            print("hhh")
            return 2
    else:
        print("Not fpund")
        return 0


def update_cuopon_status(customer):
    if CouponStatus.objects.filter(customer=customer, is_applied=True).exists():
        CouponStatus.objects.filter(customer=customer, is_applied=True).update(status=True)
        print("celard all")
    return True


def get_order_total(order_id):
    order_instance = Order.objects.get(pk=order_id)
    instances = OrderItem.objects.filter(order=order_instance)
    customer = order_instance.customer
    amt = 0
    total_cgst = 0
    total_sgst = 0
    total_igst = 0
    extras = Extras.objects.get(pk=1)

    inter_state_rate = extras.inter_state_charges
    intra_state_rate = extras.intra_state_charges
    special_discount = extras.special_discount

    total = 0

    for i in instances:
        print("Product ==>", i.product_variant)
        print("Product ==>", i.qty)
        amt = decimal.Decimal(i.price) * int(i.qty)
        cgst = amt * i.product_variant.product.hsn_code.cgst_rate / 100
        sgst = amt * i.product_variant.product.hsn_code.sgst_rate / 100
        igst = amt * i.product_variant.product.hsn_code.igst_rate / 100

        total_cgst = total_cgst + cgst
        total_sgst = total_sgst + sgst
        total_igst = total_igst + igst
        delivery_fee = 0

        if CustomerAddress.objects.filter(customer=customer, is_default=True, is_deleted=False).exists():
            address = CustomerAddress.objects.get(customer=customer, is_deleted=False, is_default=True)
            if address.state == 'kerala' or address.state == 'Kerala' or address.state == 'KL':
                delivery_fee = int(intra_state_rate)
                total = amt + cgst + sgst
                print("total===>>", cgst)
            else:
                delivery_fee = int(inter_state_rate)
                total = int(i.qty) * i.product_variant.price + igst

    return total


def calculate_gst(user):
    response_data = {}

    try:
        instances = ShoppingBagItem.objects.filter(customer__user=user)

        amt = 0
        total_cgst = 0
        total_sgst = 0
        total_igst = 0

        grand_total = 0
        item_total = 0

        for i in instances:
            # calculating the gst codes
            amt = i.product_variant.price * i.qty
            cgst = amt * i.product_variant.product.gst_code.cgst_rate / 100
            sgst = amt * i.product_variant.product.gst_code.sgst_rate / 100
            igst = amt * i.product_variant.product.gst_code.igst_rate / 100

            # appended to the totals gst fields
            total_cgst = total_cgst + cgst
            total_sgst = total_sgst + sgst
            total_igst = total_igst + igst

            # total igst removed needed to be added
            grand_total += total_cgst + total_sgst
            item_total += amt

    except Exception as e:
        response_data = {"status": False, "error": str(e), }

    else:
        response_data = {
            "status": True,
            "tax": grand_total
        }

    return response_data


def get_single_total_amount(variant, qty):
    """
    get all the totals including total_amt, discount, item_total etc.
    :param customer:
    :return:
    """
    response_data = {}

    try:
        price = variant.price
        cgst = variant.product.gst_code.cgst_rate
        sgst = variant.product.gst_code.sgst_rate

        final_amt = decimal.Decimal(price) * int(qty)

        csgst_amt = decimal.Decimal(final_amt) * decimal.Decimal(cgst) / 100
        sgst_amt = decimal.Decimal(final_amt) * decimal.Decimal(sgst) / 100

        gst_totals = csgst_amt + sgst_amt



    except Exception as e:
        response_data = {"status": False, "error": str(e), }

    else:
        response_data = {
            "status": True,
            "product_total": final_amt,
            "gst": gst_totals
        }

    return response_data
