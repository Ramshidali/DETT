import datetime
from customers.models import Customer

from users.models import Notification
from general.functions import get_current_role


def main_context(request):
    today = datetime.date.today()
    is_superuser = False
    is_administrator = False
    is_customer = False
    
    current_role = get_current_role(request)
    
    if "set_user_timezone" in request.session:
        user_session_ok = True
        user_time_zone = request.session['set_user_timezone']
    else:
        user_session_ok = False
        user_time_zone = "Asia/Kolkata"

    current_theme = 'teal'
    
    if request.user.is_authenticated:
        recent_notifications = Notification.objects.filter(user=request.user,is_deleted=False)
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            is_customer = True
    else:
        recent_notifications = []
        

    active_parent = request.GET.get('active_parent')
    active = request.GET.get('active')
    
    if current_role == "superadmin":
        is_superuser = True
    elif current_role == "administrator":
        is_administrator = True
        

    return {
        'app_title' : "Default Application",
        "user_session_ok" : user_session_ok,
        "user_time_zone" : user_time_zone,
        "confirm_delete_message" : "Are you sure want to delete this item. All associated data may be removed.",
        "revoke_access_message" : "Are you sure to revoke this user's login access",
        "confirm_shop_delete_message" : "Your shop will deleted permanently. All data will lost.",
        "confirm_delete_selected_message" : "Are you sure to delete all selected items.",
        "confirm_read_message" : "Are you sure want to mark as read this item.",
        "confirm_read_selected_message" : "Are you sure to mark as read all selected items.",
        'domain' : request.META['HTTP_HOST'],
        "current_theme" : current_theme,
        "is_customer" : is_customer,
        "is_superuser" : is_superuser,
        "is_administrator" : is_administrator,
        "active_parent" : active_parent,
        "active_menu" : active,
        "recent_notifications" : recent_notifications,
    }
