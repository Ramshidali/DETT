from django.urls import re_path

from . import views

app_name = 'orders'

urlpatterns = [
    re_path(r'^$', views.orders, name='orders'),
    re_path(r'^cancelled-orders/$', views.cancelled_orders, name='cancelled_orders'),
    re_path(r'^completed-orders/$', views.completed_orders, name='completed_orders'),
    re_path(r'^order/(?P<pk>.*)$', views.order, name='order'),
    re_path(r'^assign-charges/(?P<pk>.*)$', views.assign_charges, name='assign_charges'),

]
