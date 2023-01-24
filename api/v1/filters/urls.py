from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    re_path(r'^get-filter-params/$', views.get_category, name='get_category'),
    re_path(r'^get-color/$', views.get_color, name='get_color'),
    re_path(r'^get-brand/$', views.get_brand, name='get_brand'),
    re_path(r'^apply-filter/$', views.apply_filter, name='apply_filter'),

    re_path(r'^save-search/(?P<pk>.*)$', views.save_search, name='save_search'),
    re_path(r'^get-search/$', views.get_search, name='get_search'),

    re_path(r'^save-person/$', views.save_person, name='save_person'),
    re_path(r'^save-delivery-date/$', views.save_delivery_date, name='save_delivery_date'),

    re_path(r'^get-images/$', views.get_images, name='get_images'),

]
