from django.urls import path, re_path, include

from general import views
from general.views import OccassionAutoComplete, SubOccassionAutoComplete, PersonTypeAutoComplete

app_name = "general"

urlpatterns = [
    re_path(r'^$', views.dashboard, name='dashboard'),

    re_path(r'^create-occassion/$', views.create_occassion, name='create_occassion'),
    re_path(r'^occassion/(?P<pk>.*)$', views.occassion, name='occassion'),
    re_path(r'^occassions/$', views.occassions, name='occassions'),
    re_path(r'^edit-occassion/(?P<pk>.*)$', views.edit_occassion, name='edit_occassion'),
    re_path(r'^delete-occassion/(?P<pk>.*)$', views.delete_occassion, name='delete_occassion'),

    re_path(r'^create-sub-occassion/$', views.create_sub_occassion, name='create_sub_occassion'),
    re_path(r'^sub-occassion/(?P<pk>.*)$', views.sub_occassion, name='sub_occassion'),
    re_path(r'^sub-occassions/$', views.sub_occassions, name='sub_occassions'),
    re_path(r'^edit-sub-occassion/(?P<pk>.*)$', views.edit_sub_occassion, name='edit_sub_occassion'),
    re_path(r'^delete-sub-occassion/(?P<pk>.*)$', views.delete_sub_occassion, name='delete_sub_occassion'),

    re_path(r'^create-coupon/$', views.create_coupon, name='create_coupon'),
    re_path(r'^coupon/(?P<pk>.*)$', views.coupon, name='coupon'),
    re_path(r'^coupons/$', views.coupons, name='coupons'),
    re_path(r'^edit-coupon/(?P<pk>.*)$', views.edit_coupon, name='edit_coupon'),
    re_path(r'^delete-coupon/(?P<pk>.*)$', views.delete_coupon, name='delete_coupon'),

    re_path(r'^create-person-type/$', views.create_person_type, name='create_person_type'),
    re_path(r'^person-type/(?P<pk>.*)$', views.person_type, name='person_type'),
    re_path(r'^person-types/$', views.person_types, name='person_types'),
    re_path(r'^edit-person-type/(?P<pk>.*)$', views.edit_person_type, name='edit_person_type'),
    re_path(r'^delete-person-type/(?P<pk>.*)$', views.delete_person_type, name='delete_person_type'),

    re_path(r'^create-due-day/$', views.create_due_day, name='create_due_day'),
    re_path(r'^due-day/(?P<pk>.*)$', views.due_day, name='due_day'),
    re_path(r'^due-days/$', views.due_days, name='due_days'),
    re_path(r'^edit-due-day/(?P<pk>.*)$', views.edit_due_day, name='edit_due_day'),
    re_path(r'^delete-due-day/(?P<pk>.*)$', views.delete_due_day, name='delete_due_day'),

    re_path(r'^create-phone/$', views.create_phone, name='create_phone'),
    re_path(r'^phones/$', views.phones, name='phones'),
    re_path(r'^edit-phone/(?P<pk>.*)$', views.edit_phone, name='edit_phone'),

    re_path(r'^create-you-moment/$', views.create_image, name='create_image'),
    re_path(r'^you-moments/$', views.images, name='images'),
    re_path(r'^edit-you-moment/(?P<pk>.*)$', views.edit_image, name='edit_image'),
    re_path(r'^delete-you-moment/(?P<pk>.*)$', views.delete_image, name='delete_image'),

    re_path(r'^edit-charge/(?P<pk>.*)$', views.extras, name='extras'),

    re_path(r'^create-banner/$', views.create_slider, name='create_slider'),
    re_path(r'^banners/$', views.sliders, name='sliders'),
    re_path(r'^banner/(?P<pk>.*)$', views.slider, name='slider'),
    re_path(r'^delete-banner/(?P<pk>.*)$', views.delete_slider, name='delete_slider'),
    re_path(r'^edit-banner/(?P<pk>.*)$', views.edit_slider, name='edit_slider'),

    re_path(r'^occassion-autocomplete/$', OccassionAutoComplete.as_view(), name='occassion_autocomplete', ),
    re_path(r'^sub-occassion-autocomplete/$', SubOccassionAutoComplete.as_view(), name='sub_occassion_autocomplete', ),
    re_path(r'^person-type-autocomplete/$', PersonTypeAutoComplete.as_view(), name='person_type_autocomplete', ),
]
