from django.urls import re_path

from . import views

app_name = 'delivery_agents'

urlpatterns = [
    re_path(r'^$', views.delivery_agents, name='delivery_agents'),
    re_path(r'^create-agent/$', views.create_agent, name='create_agent'),
    re_path(r'^agent/(?P<pk>.*)$', views.agent, name='agent'),
    re_path(r'^edit-agent/(?P<pk>.*)$', views.edit_agent, name='edit_agent'),
    re_path(r'^delete-agent/(?P<pk>.*)$', views.delete_agent, name='delete_agent'),
]
