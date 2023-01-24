#Standard
import string
import random
import random
import string
import requests
from cryptography.fernet import Fernet
#Django
from django.core.exceptions import ImproperlyConfigured
from mailqueue.models import MailerMessage
from django.conf import settings
import requests



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_id(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_form_errors(args,formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors  + "|"
        for err in args.non_field_errors():
            message += str(err) + "|"

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message +=field.errors + "|"
            for err in form.non_field_errors():
                message += str(err) + "|"
    return message[:-1]


def get_auto_id(model):
    auto_id = 1
    latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def get_timezone(request):
    if "set_user_timezone" in request.session:
        user_time_zone = request.session['set_user_timezone']
    else:
        user_time_zone = "Asia/Kolkata"
    return user_time_zone


def get_current_role(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            current_role = "superadmin"
        else:
            current_role = "user"

    else:
        if 'userRole' in request.session:
            current_role = request.session['userRole']
        else:
            current_role = "AnonymousUser"

    return current_role

def send_sms():
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {"authorization":"Sj8KZSZJBefOcjVjnSrv5KAEORR4bkaEhahUCfCehAs2WN7gXhfSwCsJDelB",
                   "variables_values":"","route":"dlt",
                   "sender_id": "DETTPL",
                   "numbers":"86068760556,",
                   "message": "138002"}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)


def send_email(subject,to_address,content,bcc_address=settings.DEFAULT_BCC_EMAIL,app="dett",reply_to_address=settings.DEFAULT_REPLY_TO_EMAIL,attachment=None):
    print("send fun")
    new_message = MailerMessage()
    new_message.subject = subject
    new_message.to_address = to_address
    if bcc_address:
        new_message.bcc_address = bcc_address
    new_message.from_address = settings.DEFAULT_FROM_EMAIL
    new_message.content = content
    # new_message.html_content = html_content
    new_message.app = app
    if attachment:
        new_message.add_attachment(attachment)
    new_message.subjectreply_to = reply_to_address
    new_message.save()


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()