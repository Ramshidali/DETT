from django.urls import path, re_path, include

from web import views

app_name = "web"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    
    re_path(r'^otp-generation/$', views.otp_generation, name='otp_generation'),
    re_path(r'^otp-verification/$', views.verify_otp, name='verify_otp'),
    
    re_path(r'^profile/', views.profile, name='profile'),
    re_path(r'^user-logout/', views.user_logout, name='logout'),
    re_path(r'^edit-address/(?P<pk>.*)$', views.edit_address, name='edit_address'),
    re_path(r'^update-address/(?P<pk>.*)$', views.update_address, name='update_address'),
    
    re_path(r'^gifts/', views.gifts, name='gifts'),
    re_path(r'^terms/', views.terms, name='terms'),
    re_path(r'^privacy/', views.privacy, name='privacy'),
    re_path(r'^return/', views.return_policy, name='return'),
    re_path(r'^delivery/', views.delivery, name='delivery'),
    re_path(r'^product/(?P<pk>.*)$', views.product, name='product'),
    
    re_path(r'^buy-now-address/(?P<pk>.*)$', views.buy_now_address, name='buy_now_address'),
    re_path(r'^buy-now-single/(?P<pk>.*)$', views.buy_now_address_next, name='buy_now_address_next'),
    
    re_path(r'^add-address/(?P<pk>.*)$', views.buy_now_add_address, name='buy_now_add_address'),
    re_path(r'^add-default-address/(?P<pk>.*)$', views.set_default_address, name='set_default_address'),
    re_path(r'^place-order/(?P<pk>.*)/$', views.place_order, name='place_order'),
    re_path(r'^payment-gateway/(?P<order_id>.*)/$', views.payment_gateway, name='payment_gateway'),
    
    re_path(r'^payment-response/(?P<order_id>.*)/$', views.payment_response, name="payment_response"),
    re_path(r'^payment-success/(?P<order_id>.*)/$', views.payment_success, name="payment_success"),
]