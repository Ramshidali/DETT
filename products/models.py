from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from general.models import Occassion, SubOccassion, BaseModel, PersonType, UserBaseModel
from versatileimagefield.fields import VersatileImageField
from customers.models import Customer
from django.utils.translation import ugettext_lazy as _


GST_CODE_CHOICES = (
    ('hsn', 'HSN'),
    ('sac', 'SAC'),
)

AGE = (
    ("all", "All"),
    ("10", "0-9"),
    ("20", "10-19"),
    ("30", "20-29"),
    ("40", "30-39"),
    ("50", "40-49"),
    ("60", "50-59"),
    ("70", "60-69"),
    ("80", "70-79"),
    ("90", "80 and above"),
)

GENDER = (
    ("10", "Male"),
    ("20", "Female"),
    ("30", "Other"),
)

class ProductCategory(BaseModel):
    category_name = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=256, null=False)
    category_image = VersatileImageField(upload_to="products/category/images/", null=True,blank=True)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.category_name


class GstCodes(BaseModel):
    type= models.CharField(max_length=256,choices=GST_CODE_CHOICES,null=True,blank=True)
    code = models.CharField(max_length=128)
    igst_rate = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[
        MinValueValidator(Decimal('0.00'))])
    sgst_rate = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[
        MinValueValidator(Decimal('0.00'))])
    cgst_rate = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[
        MinValueValidator(Decimal('0.00'))])

    class Meta:
        verbose_name = _('product hsn code')
        verbose_name_plural = _('product hsn codes')

    def __str__(self):
        return f"{self.type} - {self.code}"


class Product(BaseModel):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False)
    feautured_image = VersatileImageField(upload_to="products/images/",null=True,blank=True)
    product_description = models.CharField(max_length=256, null=False)
    meta_description = models.CharField(max_length=256, null=False)
    gst_code = models.ForeignKey(GstCodes, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class UnitOfMeasurement(BaseModel):
    unit_of_measurement = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('unit_of_measurement',)
        verbose_name = 'unit of measurment'
        verbose_name_plural = 'unit of measurements'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated',)

    def __str__(self):
        return self.unit_of_measurement


class Unit(BaseModel):
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    unit = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('unit',)
        verbose_name = 'unit'
        verbose_name_plural = 'units'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated',)

    def __str__(self):
        return self.unit


class ProductColor(UserBaseModel):
    color = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('color',)
        verbose_name = 'product color'
        verbose_name_plural = 'product colors'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated',)

    def __str__(self):
        return self.color


class Brand(UserBaseModel):
    brand = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('brand',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated',)

    def __str__(self):
        return self.brand


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    uom = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    mrp = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    opening_stock = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                        validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    stock = models.DecimalField(default=0.0, decimal_places=2, max_digits=15,
                                validators=[MinValueValidator(Decimal('0.00'))])
    gender = models.CharField(max_length=256,choices=GENDER)
    age_group = models.CharField(max_length=256,choices=AGE)
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE,null=True,blank=True)
    is_default = models.BooleanField(default=False)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'product variant'
        verbose_name_plural = 'product variants'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated',)

    def __str__(self):
        return self.title

    def get_full_name(self):
        return f"{self.product.name} - {self.title}"

    def product_name(self):
        return f"{self.product.name}"
    

class ProductImage(BaseModel):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    feautured_image = VersatileImageField(upload_to="products/products/images/", null=True,blank=True)

    class Meta:
        ordering = ('feautured_image',)
        verbose_name = 'product_image'
        verbose_name_plural = 'product images'
        # exclude = ('creator', 'updater', 'date_added', 'date_updated')

    def __str__(self):
        return self.product_variant.title


class ProductForOccassion(BaseModel):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    occassion = models.ForeignKey(Occassion, on_delete=models.CASCADE)
    sub_occassion = models.ForeignKey(SubOccassion, on_delete=models.CASCADE)
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE)

    class Meta:
        ordering = ('occassion',)
        verbose_name = 'occassion'
        verbose_name_plural = 'occassions'

    def __str__(self):
        return self.sub_occassion.sub_occassion


class RecentSearches(BaseModel):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        ordering = ('product',)
        verbose_name = 'recent search'
        verbose_name_plural = 'recent searches'
