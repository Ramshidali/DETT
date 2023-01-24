from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from general import views as general_views

admin.site.enable_nav_sidebar = False

urlpatterns = [
    re_path(r'^dett-admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', include('web.urls')),
    path('app/dashboard/', general_views.dashboard, name='dashboard'),
    path('app/accounts/', include('registration.backends.default.urls')),

    path('users/', include('users.urls')),
    path('app/', general_views.app, name='app'),
    path('app/general/', include('general.urls')),
    path('app/products/', include('products.urls')),
    path('app/customers/', include('customers.urls')),
    path('app/delivery_agents/', include('delivery_agents.urls')),
    path('app/orders/', include('orders.urls')),
    path('app/staffs/', include('staffs.urls')),
    path('app/promotions/', include('promotions.urls')),
    path('app/reports/', include('reports.urls')),

    re_path('api/v1/auth/',
            include(('api.v1.authentication.urls', 'authentication'), namespace='api_v1_authentication')),
    re_path('api/v1/register/',
            include(('api.v1.registrations.urls', 'registrations'), namespace='api_v1_registrations')),
    re_path('api/v1/users/',
            include(('api.v1.users.urls', 'users'), namespace='api_v1_users')),
    re_path('api/v1/orders/',
            include(('api.v1.orders.urls', 'users'), namespace='api_v1_orders')),
    re_path('api/v1/filters/',
            include(('api.v1.filters.urls', 'users'), namespace='api_v1_filters')),

    re_path('api/v1/promotions/',
            include(('api.v1.promotions.urls', 'promotions'), namespace='api_v1_promotions')),


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_FILE_ROOT})
]
