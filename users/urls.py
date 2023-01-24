from django.urls import re_path

from . import views


app_name = 'users'


urlpatterns = [
    re_path(r'^$', views.dashboard, name='dashboard'),

    re_path(r'^notifications/$', views.notifications, name='notifications'),
    re_path(r'^check-notification/$', views.check_notification, name='check_notification'),
    re_path(r'^notification/read/(?P<pk>.*)/$', views.read_notification, name='read_notification'),
    re_path(r'^notification/delete/(?P<pk>.*)/$', views.delete_notification, name='delete_notification'),
    re_path(r'^read-selected-notifications/$', views.read_selected_notifications, name='read_selected_notifications'),
    re_path(r'^delete-selected-notifications/$', views.delete_selected_notifications, name='delete_selected_notifications'),

    re_path(r'^set-user-timezone/$', views.set_user_timezone, name='set_user_timezone'),
]
