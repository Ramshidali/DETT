from django.urls import path, re_path, include

from reports import views

app_name = "reports"

urlpatterns = [
    re_path(r'^gst-r1-report/$', views.gstr1_report, name='gstr1_report'),
]
