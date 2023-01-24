from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register-number/$', views.register_number, name='register_number'),
    url(r'^otp-verify/$', views.verify_otp, name='verify_otp'),
    url(r'^register/$', views.register, name='register'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^send-otp/$', views.send_otp, name='send_otp'),
    url(r'^login-with-otp/$', views.login_with_otp, name='login_with_otp'),

    url(r'^reset-password/$', views.reset_password, name='reset_password'),
    url(r'^change-number/$', views.change_number, name='change_number'),
    url(r'^change-number-update/$', views.change_number_update, name='change_number_update'),

    url(r'^get-profile/$', views.get_profile, name='get_profile'),
    url(r'^update-name/$', views.update_name, name='update_name'),
    url(r'^change-email/$', views.change_email, name='change_email'),
    url(r'^change-email-update/$', views.change_email_update, name='change_email_update'),
    url(r'^update-profile-pic/$', views.update_profile_pic, name='update_profile_pic'),

]
