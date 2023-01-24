from django.contrib import admin

from customers.models import Customer,CustomerAddress,Otp,OtpMail,MomentCard, Moments

admin.site.register(Customer)
admin.site.register(CustomerAddress)
admin.site.register(Otp)
admin.site.register(OtpMail)
admin.site.register(MomentCard)
admin.site.register(Moments)

