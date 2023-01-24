from django.conf.urls import url, re_path

from . import views

urlpatterns = [

    re_path(r'^place-order/$', views.place_order, name='place_order'),
    re_path(r'^view-single-order-product/(?P<pk>.*)$', views.view_single_order_product, name='view_single_order_product'),
    re_path(r'^single-order-product-update-qty/(?P<pk>.*)$', views.single_order_product_update_qty,
            name='single_order_product_update_qty'),

    re_path(r'^place-single-order/$', views.place_single_order, name='place_single_order'),
    re_path(r'^get-orders/$', views.get_orders, name='get_orders'),
    # re_path(r'^search-orders/$', views.search_orders, name='search_orders'),

    re_path(r'^check-product/$', views.check_product, name='check_product'),

    re_path(r'^get-single-order/(?P<pk>.*)$', views.get_single_order, name='get_single_order'),
    re_path(r'^track-order/(?P<pk>.*)$', views.track_order, name='track_order'),
    re_path(r'^rate-order/(?P<pk>.*)$', views.rate_order, name='rate_order'),
    re_path(r'^cancel-order/(?P<pk>.*)$', views.cancel_order, name='cancel_order'),
    re_path(r'^download-invoice/(?P<pk>.*)$', views.download_invoice, name='download_invoice'),

    re_path(r'^order-notifications/$', views.order_notifications, name='order_notifications'),

]
