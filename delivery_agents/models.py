from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from general.models import UserBaseModel

gender = (
    ('10', 'Male'),
    ('20', 'Female'),
    ('30', 'Others'),
)
UserModel = get_user_model()


class DeliveryAgent(UserBaseModel):
    name = models.CharField(max_length=256, null=False)
    email = models.EmailField()
    joining_date = models.DateField(null=True)
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField(null=True)
    gender = models.CharField(choices=gender, null=True,max_length=256)
    salary = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                 validators=[MinValueValidator(Decimal('0.00'))])
    location = models.CharField(null=True,max_length=256)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'delivery agent'
        verbose_name_plural = 'delivery agents'

    def __str__(self):
        return self.name
