from django.contrib.auth import get_user_model
from django.db import models

from general.models import BaseModel

UserModel = get_user_model()


class Designation(BaseModel):
    name = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'staff designation'
        verbose_name_plural = 'staffs designation'

    def __str__(self):
        return self.name


class Staff(BaseModel):
    name = models.CharField(max_length=256, null=False)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField(max_length=256, null=True, blank=True)
    bank_name = models.TextField(max_length=256, null=True, blank=True)
    branch = models.TextField(max_length=256, null=True, blank=True)
    bank_account_name = models.TextField(max_length=256, null=True, blank=True)
    ifsc_code = models.TextField(max_length=256, null=True, blank=True)
    account_number = models.TextField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'staff designation'
        verbose_name_plural = 'staffs designation'

    def __str__(self):
        return self.name
