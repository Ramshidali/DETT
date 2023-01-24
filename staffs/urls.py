from django.urls import path, re_path, include

from staffs.views import DesignationAutoComplete
from staffs import views

app_name = "staffs"

urlpatterns = [
    re_path(r'^$', views.designations, name='designations'),
    re_path(r'^create-designation/$', views.create_designation, name='create_designation'),
    re_path(r'^designation/(?P<pk>.*)$', views.designation, name='designation'),
    re_path(r'^edit-designation/(?P<pk>.*)$', views.edit_designation, name='edit_designation'),
    re_path(r'^delete-designation/(?P<pk>.*)$', views.delete_designation, name='delete_designation'),

    re_path(r'^staffs/$', views.staffs, name='staffs'),
    re_path(r'^create-staff/$', views.create_staff, name='create_staff'),
    re_path(r'^staff/(?P<pk>.*)$', views.staff, name='staff'),
    re_path(r'^edit-staff/(?P<pk>.*)$', views.edit_staff, name='edit_staff'),
    re_path(r'^delete-staff/(?P<pk>.*)$', views.delete_staff, name='delete_staff'),

    re_path(r'^designation-autocomplete/$', DesignationAutoComplete.as_view(), name='designation_autocomplete', ),
]
