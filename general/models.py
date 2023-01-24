import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey("auth.User", blank=True, related_name="creator_%(class)s_objects",
                                on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, related_name="updater_%(class)s_objects",
                                on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Mode(models.Model):
    readonly = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    down = models.BooleanField(default=False)

    class Meta:
        db_table = 'mode'
        verbose_name = _('mode')
        verbose_name_plural = _('mode')
        ordering = ('id',)

    class Admin:
        list_display = ('id', 'readonly', 'maintenance', 'down')

    def __unicode__(self):
        return str(self.id)


class PersonType(BaseModel):
    person_type = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('person_type',)
        verbose_name = 'person type'
        verbose_name_plural = 'person types'

    def __str__(self):
        return self.person_type


class Phone(models.Model):
    phone = models.TextField(max_length=125)

    class Meta:
        db_table = 'phone'
        verbose_name = 'phone'
        verbose_name_plural = 'phone'

    def __int__(self):
        return self.phone


class SetDueDays(BaseModel):
    no_of_days = models.CharField(max_length=12, null=False)

    class Meta:
        ordering = ('no_of_days',)
        verbose_name = 'Due days'
        verbose_name_plural = 'due days'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated', 'auto_id',)

    def __int__(self):
        return self.no_of_days


class SetCoupon(BaseModel):
    coupon_code = models.CharField(max_length=250, null=False)
    offer_percentage = models.CharField(max_length=250, null=False)
    title  = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('coupon_code',)
        verbose_name = 'coupon'
        verbose_name_plural = 'coupons'

    def __str__(self):
        return self.coupon_code


class Occassion(BaseModel):
    occassion = models.CharField(max_length=256, null=False)
    occassion_image = VersatileImageField(upload_to="lessons/images/", null=True,blank=True)

    class Meta:
        ordering = ('occassion',)
        verbose_name = 'occassion'
        verbose_name_plural = 'occassions'

    def __str__(self):
        return self.occassion


class SubOccassion(BaseModel):
    occassion = models.ForeignKey(Occassion, on_delete=models.CASCADE, )
    sub_occassion = models.CharField(max_length=256, null=False)
    sub_occassion_image = VersatileImageField(upload_to="occasion/subocassions/images/",null=True,blank=True)

    class Meta:
        ordering = ('occassion',)
        verbose_name = 'sub occassion'
        verbose_name_plural = 'sub occassions'

    def __str__(self):
        return self.sub_occassion


class GiftImage(BaseModel):
    image = VersatileImageField(upload_to="gifts/images/", null=True,blank=True)

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.image.url

class Extras(models.Model):
    inter_state_charges = models.FloatField()
    intra_state_charges = models.FloatField()
    special_discount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Charges and Discounts'
        verbose_name_plural = 'Charges and Discounts'

    def __str__(self):
        return self.special_discount



class Slider(BaseModel):
    title = models.CharField(max_length=250, null=False)
    image = VersatileImageField(upload_to="slider/images/", null=True,blank=True)

    class Meta:
        verbose_name = 'slider'
        verbose_name_plural = 'sliders'
        ordering = ('auto_id',)


    def __str__(self):
        return self.title