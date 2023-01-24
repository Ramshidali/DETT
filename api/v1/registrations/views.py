import email
import base64

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from api.v1.general.functions import get_otp, check_paswword_strength, get_user_token, generate_serializer_errors, \
    get_user
from api.v1.registrations.serializers import RegisterCustomerSerializer, UserSerializer, OtpVerifySerializer, \
    RegisterSerializer, CustomerSerializer
from customers.models import Customer, Otp, OtpMail
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.shortcuts import (get_object_or_404, )
from general.functions import get_auto_id, send_email
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from users.functions import encrypt_message, decrypt_message
from general.utils.sms import SMS

@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def register(request):
    otp = get_otp()
    message = ""
    error = False

    serialized = RegisterSerializer(data=request.data)

    username = request.data['username']
    password = request.data['password']
    email = request.data['email']

    if User.objects.filter(username=username, is_active=True).exists():
        error = True
        message += "A User with this Phone Number already exists."

    if User.objects.filter(email=email, is_active=True).exists():
        error = True
        message += "A User with this Email already exists."

    if Customer.objects.filter(phone=username, is_deleted=False, user__is_active=True).exists():
        error = True
        message += "This Phone Number already exists."

    if not error:
        if serialized.is_valid():
            # password = make_password(password)
            if Otp.objects.filter(phone=username).exists():
                otp = Otp.objects.get(phone=username).otp

            data = User.objects.create_user(
                username=username,
                password=password,
                is_active=True,
            )

            instance = data

            customer = Customer.objects.create(
                user=instance,
                auto_id=get_auto_id(Customer),
                creator=instance,
                updater=instance,
                phone=username,
                otp=otp,
                email=email,
                password=encrypt_message(password),
            )

            response = get_user_token(request, username, password)

            response_data = {
                "StatusCode": 6000,
                "token": response.json(),
                "data": serialized.data,
                "otp": str(otp),
                "message": "Account Created Successfully"
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "message": generate_serializer_errors(serialized._errors)
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": message
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def register_number(request):
    """
    The first signup functions
    :param request:
    :return:
    """
    serialized = OtpVerifySerializer(data=request.data)
    s = request.data
    data = request.data
    phone = data['phone']

    if serialized.is_valid():
        otp = get_otp()
        sms_manager = SMS(phone)

        if Customer.objects.filter(phone=phone).exists():

            response_data = {
                "StatusCode": 6001,
                "message": "User Already Registered, Please Sign in"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            sms_manager.send_otp(otp)
            if Otp.objects.filter(phone=phone).exists():
                serialized.updateOtp(phone,otp)
            else:
                serialized.save(otp=otp)

            response_data = {
                "StatusCode": 6000,
                'data': serialized.data,
                'otp': str(otp),
                "message": "OTP Sent Successfully"
            }

            return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": serialized.errors
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def verify_otp(request):
    serialized = OtpVerifySerializer(data=request.data)
    otp = serialized.verify_otp(request.data)
    # print("kkoo==>>",otp)
    if otp is True:
        response_data = {
            "StatusCode": 6000,
            "message": "OTP verified"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        # print("looooo")
        response_data = {
            "StatusCode": 6001,
            "message": "Invalid OTP or timeout"
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def send_otp(request):
    data = request.data
    phone = data['phone']
    new_otp = get_otp()

    sms_manager = SMS(phone)

    if Customer.objects.filter(phone=phone).exists():
        sms_manager.send_otp(new_otp)
        Customer.objects.filter(phone=phone).update(otp=new_otp)

        response_data = {
            "StatusCode": 6000,
            "otp": new_otp,
            "message": "OTP Send Successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Phone Number not found"
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def login_with_otp(request):
    data = request.data
    phone = data['phone']
    otp = data['otp']
    customer_instance = None
    user = User.objects.get(username=phone)
    # print("[[=====", user)

    if Customer.objects.filter(phone=phone).exists():
        customer_instance = Customer.objects.get(phone=phone)
        # print("OTP is ==>>",otp)
    if customer_instance.otp == otp:

        response = get_user_token(
            request, customer_instance.phone, decrypt_message(customer_instance.password))

        response_data = {
            "StatusCode": 6000,
            "token": response.json(),
            "message": "Successfully logged in"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Invalid OTP"
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def reset_password(request):
    data = request.data
    phone = data['phone']
    new_password = data['password']

    customer_instance = None
    user = User.objects.get(username=phone)

    if Customer.objects.filter(phone=phone).exists():
        customer_instance = Customer.objects.get(phone=phone)

    user.set_password(new_password)
    user.save()

    response = get_user_token(request, customer_instance.phone, new_password)

    response_data = {
        "StatusCode": 6000,
        "token": response.json(),
        "message": "Password Successfully Resets "
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_password(request):
    user = get_user(request.user)
    req_user = User.objects.get(username=user.phone)

    old_password = request.data['old_password']
    new_password = request.data['new_password']

    if req_user.check_password(old_password):
        req_user.set_password(new_password)
        req_user.save()
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Invalid Existing Password"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6000,
        "message": "Password Changed Successfully"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_number(request):
    user = get_user(request.user)
    req_user = User.objects.get(username=user.phone)
    old_phone = Customer.objects.get(phone=user.phone)
    new_phone = request.data['new_phone']
    
    if not User.objects.filter(username=new_phone).exists() :

        if Otp.objects.filter(phone=new_phone).exists():
            new_otp = get_otp()
            print("+ new ", new_otp)
            Otp.objects.filter(phone=new_phone).update(otp=new_otp)
        else:
            otp = get_otp()
            print("+ old ", otp)
            Otp.objects.create(phone=new_phone, otp=otp)

        old_phone_otp = get_otp()
        Customer.objects.filter(phone=old_phone.phone).update(otp=old_phone_otp)

        response_data = {
            "StatusCode": 6000,
            "message": "OTP sended"
        }
    else:        
        response_data = {
            "StatusCode": 6001,
            "message": "Phone Number Already Existed"
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_number_update(request):
    message = ""
    error = False

    user = get_user(request.user)
    req_user = User.objects.get(username=user.phone)
    old_phone = Customer.objects.get(phone=user.phone)

    new_phone = request.data['new_phone']
    new_phone_instance = Otp.objects.get(phone=new_phone)

    data = request.data
    new_otp = data['new_otp']
    # old_otp = data['old_otp']
    password = data['password']

    # old_phone_otp = old_phone.otp
    new_phone_otp = new_phone_instance.otp

    if new_otp != new_phone_otp:
        error = True
        message += "OTP incorrect " + new_phone

    # if old_phone_otp != old_otp:
    #     error = True
    #     message += "OTP incorrect " + old_phone.phone

    if password != decrypt_message(old_phone.password):
        error = True
        message += "Invalid Password"
        
    if not error:
        req_user.username = new_phone
        req_user.save()
        Customer.objects.filter(phone=user.phone).update(phone=new_phone)

        response_data = {
            "StatusCode": 6000,
            "message": "Phone Number Updated"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:

        response_data = {
            "StatusCode": 6001,
            "message": message
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_profile(request):
    user = get_user(request.user)
    instances = None
    if Customer.objects.filter(phone=user).exists():
        instances = Customer.objects.get(phone=user)

    serialized = CustomerSerializer(instances,context={"request":request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update_name(request):
    user = get_user(request.user)
    data = request.data
    name = data['name']
    last_name = data['last_name']

    if Customer.objects.filter(phone=user).exists():
        Customer.objects.filter(phone=user).update(name=name, last_name=last_name)

    response_data = {
        "StatusCode": 6000,
        "message": "Name updated"
    }

    return Response(response_data, status=status.HTTP_200_OK)


#
#
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def change_email(request):
#     user = get_user(request.user)
#     req_user = User.objects.get(username=user.phone)
#     old_email = Customer.objects.get(phone=user.phone)
#     new_email = request.data['new_email']
#
#     if OtpMail.objects.filter(email=new_email).exists():
#         new_otp = get_otp()
        # print("+ new ",new_otp)
#         OtpMail.objects.filter(phone=new_email).update(otp=new_otp)
#     else:
#         otp = get_otp()
        # print("+ old ", otp)
#         OtpMail.objects.create(email=new_email, otp=otp)
#
#     old_email_otp = get_otp()
#     Customer.objects.filter(phone=old_email.phone).update(otp=old_email_otp)
#
#     response_data = {
#         "StatusCode": 6000,
#         "message": "OTP sended to the mail"
#     }
#
#     return Response(response_data, status=status.HTTP_200_OK)
#


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_email(request):
    user = get_user(request.user)
    req_user = User.objects.get(username=user.phone)
    old_phone = Customer.objects.get(phone=user.phone)
    new_email = request.data['new_email']
    
    if not Customer.objects.filter(email=new_email).exists():
        if OtpMail.objects.filter(email=new_email).exists():
            otp = get_otp()
            print("+ new ", otp)
            OtpMail.objects.filter(email=new_email).update(otp=otp)
        else:
            otp = get_otp()
            print("+ old ", otp)
            OtpMail.objects.create(email=new_email, otp=otp)
            
        message = f"Dear customer, {otp} is your OTP from Dett. Don't share your OTP with anyone."
        send_email("Dett user varification",new_email,message)
        old_phone_otp = get_otp()
        Customer.objects.filter(phone=old_phone.phone).update(otp=old_phone_otp)

        response_data = {
            "StatusCode": 6000,
            "message": "OTP sended"
        }
    else :
        response_data = {
            "StatusCode": 6001,
            "message": "Email already Existed"
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def change_email_update(request):
    message = ""
    error = False

    user = get_user(request.user)
    req_user = User.objects.get(username=user.phone)
    old_email = Customer.objects.get(phone=user.phone)

    new_email = request.data['new_email']
    new_email_instance = OtpMail.objects.get(email=new_email)

    data = request.data
    new_otp = data['new_otp']
    # old_otp = data['old_otp']
    password = data['password']

    # old_email_otp = old_email.otp
    new_email_otp = new_email_instance.otp

    if new_otp != new_email_otp:
        error = True
        message += "OTP incorrect " + new_email

    # if old_email_otp != old_otp:
    #     error = True
    #     message += "OTP incorrect " + old_email.phone

    if password != decrypt_message(old_email.password):
        error = True
        message += "Password is invalid"

    if not error:
        Customer.objects.filter(phone=user.phone).update(email=new_email)

        response_data = {
            "StatusCode": 6000,
            "message": "New Email Updated"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:

        response_data = {
            "StatusCode": 6001,
            "message": message
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update_profile_pic(request):
    image = request.data['image']
    
    try:
        image = ContentFile(base64.b64decode(image), name="image.png")
        request.data["image"] = image
    except:
        pass
    
    # Save and take image uri
    if (image):
        name = request.data["image"].name
        fs = FileSystemStorage()
        # print(type(fs.base_location),"--fs.base_location")
            
        fs.base_location = f"{fs.base_location}/customer/profile_images/"
        filename = fs.save(name, image)
        uploaded_file_url = 'customer/profile_images/' + filename
        
    else:
        uploaded_file_url = ""
    
    # print(image,"---image")

    if Customer.objects.filter(user=request.user).exists():
        Customer.objects.filter(user=request.user,is_deleted=False).update(image=uploaded_file_url)        

    response_data = {
        "StatusCode": 6000,
        "message": "Profile pic updated"
    }

    return Response(response_data, status=status.HTTP_200_OK)