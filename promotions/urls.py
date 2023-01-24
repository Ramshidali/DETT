from django.urls import path, re_path, include

from promotions import views


app_name = "promotions"

urlpatterns = [
    re_path(r'^enquiries/$', views.enquiries, name='enquiries'),
    re_path(r'^enquiry/(?P<pk>.*)$', views.enquiry, name='enquiry'),
    re_path(r'^mark-as-read/(?P<pk>.*)$', views.mark_as_read, name='mark_as_read'),
    re_path(r'^marked-enquiries/$', views.marked_enquiries, name='marked_enquiries'),

]