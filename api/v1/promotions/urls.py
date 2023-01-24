from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    re_path(r'^get-products/$', views.get_products, name='get_products'),
    re_path(r'^product/(?P<pk>.*)$', views.product, name='product'),
    re_path(r'^submit-enquiry/$', views.submit_enquiry, name='submit_enquiry'),
    re_path(r'^enquiries/(?P<phone>.*)$', views.get_enquiries, name='get_enquiries'),
    re_path(r'^enquiry/(?P<pk>.*)$', views.get_enquiry, name='get_enquiry'),

]
