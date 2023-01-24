from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^get-due-days/$', views.get_due_days, name='get_due_days'),

    re_path(r'^add-address/$', views.add_address, name='add_address'),
    re_path(r'^view-address/$', views.view_address, name='view_address'),
    re_path(r'^view-default-address/$', views.view_default_address, name='view_default_address'),
    re_path(r'^delete-address/(?P<pk>.*)$', views.delete_address, name='delete_address'),
    re_path(r'^edit-address/(?P<pk>.*)$', views.edit_address, name='edit_address'),
    re_path(r'^set-default-address/(?P<pk>.*)$', views.set_default_address, name='set_default_address'),

    re_path(r'^filter-gifts/$', views.filter_gifts, name='filter_gifts'),
    re_path(r'^product/(?P<pk>.*)$', views.product, name='product'),
    re_path(r'^get-sizes/(?P<pk>.*)$', views.get_sizes, name='get_sizes'),

    re_path(r'^create-moment-card/$', views.create_moment_card, name='create_moment_card'),
    re_path(r'^moment-cards/$', views.moment_cards, name='moment_cards'),
    re_path(r'^delete-moment-card/(?P<pk>.*)$', views.delete_moment_card, name='delete_moment_card'),
    re_path(r'^edit-moment-card/(?P<pk>.*)$', views.edit_moment_card, name='edit_moment_card'),

    re_path(r'^occassions/$', views.occassions, name='occassions'),
    re_path(r'^person-types/$', views.person_types, name='person_types'),

    re_path(r'^add-to-cart/(?P<pk>.*)$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^view-cart/$', views.cart, name='cart'),
    re_path(r'^change-qty/(?P<pk>.*)$', views.change_qty, name='change_qty'),
    re_path(r'^change-size/(?P<pk>.*)$', views.change_size, name='change_size'),
    re_path(r'^remove-item/(?P<pk>.*)$', views.remove_item, name='remove_item'),

    re_path(r'^get-coupons/$', views.get_coupons, name='get_coupons'),
    re_path(r'^apply-coupon/$', views.apply_coupon, name='apply_coupon'),
    re_path(r'^cancel-coupon/(?P<pk>.*)$', views.cancel_coupon, name='cancel_coupon'),

    re_path(r'^search$', views.search_product, name='search_product'),

    re_path(r'^sliders', views.sliders, name='sliders'),

    re_path(r'^occasion-single-product/(?P<pk>.*)$', views.occassion_single_product, name='occassion_single_product'),
]
