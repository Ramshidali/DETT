from django.contrib.auth import get_user_model
from django.db import models
from versatileimagefield.fields import VersatileImageField

from general.models import BaseModel, UserBaseModel, Occassion, PersonType

UserModel = get_user_model()


class Customer(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    email = models.EmailField(null=True,blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=10, null=False)
    otp = models.CharField(max_length=4, null=False)
    password = models.CharField(max_length=256,null=True)
    last_name  = models.CharField(max_length=256,null=True)
    image = VersatileImageField(upload_to="customer/profile_images/", null=True,blank=True)

    class Meta:
        ordering = ('phone',)
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.phone


class CustomerAddress(UserBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    name = models.CharField(max_length=256, null=False)
    address_line1 = models.TextField()
    phone = models.CharField(max_length=10, null=False)
    pincode = models.CharField(max_length=6, null=False)
    street = models.CharField(max_length=256, null=False)
    city = models.CharField(max_length=256, null=False)
    landmark = models.CharField(max_length=256, null=False)
    state = models.CharField(max_length=256, null=False)
    address_type = models.CharField(max_length=256, null=False)
    is_default = models.BooleanField(null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'customer adress'
        verbose_name_plural = 'customer addresses'

    def __str__(self):
        return self.name


class MomentCard(UserBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    title = models.CharField(max_length=256, null=False)
    meta = models.CharField(max_length=256, null=True,blank=True)
    occassion =  models.ForeignKey(Occassion, on_delete=models.CASCADE, )
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE, )
    person_name = models.CharField(max_length=30, null=False)
    event_date = models.DateField(max_length=6, null=False,)

    class Meta:
        ordering = ('person_name',)
        verbose_name = 'moment card'
        verbose_name_plural = 'moment cards'

    def __str__(self):
        return self.title


class Otp(models.Model):
    phone = models.CharField(max_length=256, null=False)
    otp = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('phone',)
        verbose_name = 'otp'
        verbose_name_plural = 'otp'

    def __str__(self):
        return self.phone

class OtpMail(models.Model):
    email = models.EmailField(max_length=256, null=False)
    otp = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('email',)
        verbose_name = 'email otp'
        verbose_name_plural = 'email otp'

    def __str__(self):
        return self.email

class Moments(models.Model):
    name = models.CharField(max_length=256, null=True,blank=True)
    date = models.CharField(max_length=256, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'moment'
        verbose_name_plural = 'moments'


# temp models to save delivery date
class DeliveryDateTemp(models.Model):
    date = models.CharField(max_length=256, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'delivery date temp'
        verbose_name_plural = 'delivery date temp'