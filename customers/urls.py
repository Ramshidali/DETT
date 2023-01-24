from django.urls import path, re_path, include

from customers import views

app_name = "customers"

urlpatterns = [
    re_path(r'^$', views.customers, name='customers'),
    re_path(r'^pdf/$', views.pdf, name='pdf'),

    re_path(r'^upcoming-moments/$', views.upcoming_moments, name='upcoming_moments'),

]
