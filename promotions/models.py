from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from general.models import UserBaseModel
from products.models import ProductVariant



class Enquiry(UserBaseModel):
    product = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    gift_reciever_phone = models.CharField(max_length=16, null=False)
    gift_reciever_name = models.CharField(max_length=256, null=False)
    enquirer_phone = models.CharField(max_length=16, null=False)
    enquirer_name = models.CharField(max_length=256, null=False)
    event_name = models.TextField(max_length=256, null=False)
    event_date = models.DateField()
    additional_notes = models.CharField(max_length=256, null=True,blank=True)
    source = models.CharField(max_length=256, null=False)
    enquiry_id = models.CharField(max_length=10,null=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True,null=True,blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'enquiry'
        verbose_name_plural = 'enquiries'

    def __str__(self):
        return f"{self.enquirer_name} - {self.event_name}"