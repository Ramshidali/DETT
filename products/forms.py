from dal import autocomplete
from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput, CheckboxInput
from django.utils.translation import ugettext_lazy as _

from products.models import ProductCategory, Product, UnitOfMeasurement, Unit, ProductVariant, ProductImage, \
    ProductForOccassion, ProductColor, Brand, GstCodes


TYPE = (
    ("hsn", "HSN"),
    ("sac", "SAC"),
)


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'category_name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
            'description': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Description'}),
            'category_image': FileInput()
        }

        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'description': {
                'required': _("Description field is required."),
            },
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'gst_code']

        widgets = {
            'product_category': autocomplete.ModelSelect2(url='products:category_autocomplete',
                                                          attrs={'data-placeholder': 'Category',
                                                                 'data-minimum-input-length': 1}, ),
            'name': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Name'}),
            'meta_description': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Meta'}),
            'product_description': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Description'}),
            'feautured_image': FileInput(),
        }

        error_messages = {
            'name': {
                'required': _("Product Name field is required."),
            },
            'meta_description': {
                'required': _("Meta field is required."),
            },
            'product_description': {
                'required': _("Description field is required."),
            },
            'feautured_image': {
                'required': _("Image field is required."),
            },
        }


class UomForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasurement
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'subtotal', 'total']

        widgets = {
            'unit_of_measurement': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Name'}),
        }

        error_messages = {
            'unit_of_measurement': {
                'required': _("Unit Of Measurement field is required."),
            },
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'subtotal', 'total']

        widgets = {
            'unit_of_measurement': autocomplete.ModelSelect2(url='products:uom_autocomplete',
                                                             attrs={'data-placeholder': 'Unit Of Measurement',
                                                                    'data-minimum-input-length': 1}, ),
            'unit': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Unit'}),

        }

        error_messages = {
            'unit_of_measurement': {
                'required': _("Unit Of Measurement field is required."),
            },
            'unit': {
                'required': _("Unit field is required."),
            },
        }


class PvForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'product','opening_stock']

        widgets = {
            # 'product': autocomplete.ModelSelect2(url='products:product_autocomplete',
            #                                      attrs={'data-placeholder': 'Product',
            #                                             'data-minimum-input-length': 1}, ),
            'title': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Title'}),
            'uom': autocomplete.ModelSelect2(url='products:uom_autocomplete',
                                             attrs={'data-placeholder': 'UOM',
                                                    'data-minimum-input-length': 1}, ),
            'unit': autocomplete.ModelSelect2(url='products:unit_autocomplete',
                                              attrs={'data-placeholder': 'Unit',
                                                     'data-minimum-input-length': 1}, ),
            'color': autocomplete.ModelSelect2(url='products:color_autocomplete',
                                               attrs={'data-placeholder': 'Enter a color',
                                                      'data-minimum-input-length': 1}, ),
            'brand': autocomplete.ModelSelect2(url='products:brand_autocomplete',
                                               attrs={'data-placeholder': 'Enter a brand',
                                                      'data-minimum-input-length': 1}, ),
            'mrp': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'MRP'}),
            'price': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Price'}),
            'opening_stock': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Opening Stock'}),
            'stock': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Stock'}),
            'gender': Select(attrs={'class': 'required  form-control', 'placeholder': 'Gender'},),
            'age_group': Select(attrs={'class': 'required  form-control', 'placeholder': 'Age group'},),
            'person_type': autocomplete.ModelSelect2(url='general:person_type_autocomplete',
                                                     attrs={'data-placeholder': 'Choose Person Type',
                                                            'data-minimum-input-length': 1}, ),
            'is_default': CheckboxInput()
        }

        error_messages = {
            'uom': {
                'required': _("Unit Of Measurement field is required."),
            },
            'title': {
                'required': _("Title field is required."),
            },
            'product': {
                'required': _("Product field is required."),
            },
            'mrp': {
                'required': _("MRP field is required."),
            },
            'price': {
                'required': _("Price field is required."),
            },
            'opening_stock': {
                'required': _("Opening Stock field is required."),
            },
            'stock': {
                'required': _("Stock field is required."),
            },
            'gender': {
                'required': _("Gender field is required."),
            },
            'age_group': {
                'required': _("Age Group field is required."),
            },
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted','product_variant']

        widgets = {

            'feautured_image': FileInput()
        }

        error_messages = {
            'product_variant': {
                'required': _("Product Variant field is required."),
            },
            'feautured_image': {
                'required': _("Image field is required."),
            },
        }


class ProductForOccassionForm(forms.ModelForm):
    class Meta:
        model = ProductForOccassion
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', ]

        widgets = {
            'product_variant': autocomplete.ModelSelect2(url='products:pv_autocomplete',
                                                         attrs={'data-placeholder': 'Product Variant',
                                                                'data-minimum-input-length': 1}, ),
            'occassion': autocomplete.ModelSelect2(url='general:occassion_autocomplete',
                                                   attrs={'data-placeholder': 'Choose Occassion',
                                                          'data-minimum-input-length': 1}, ),
            'sub_occassion': autocomplete.ModelSelect2(url='general:sub_occassion_autocomplete',
                                                       attrs={'data-placeholder': 'Choose Sub Occassion',
                                                              'data-minimum-input-length': 1}, ),
            'person_type': autocomplete.ModelSelect2(url='general:person_type_autocomplete',
                                                     attrs={'data-placeholder': 'Choose Person Type',
                                                            'data-minimum-input-length': 1}, ),
        }

        error_messages = {
            'product_variant': {
                'required': _("Product Variant field is required."),
            },
            'occassion': {
                'required': _("Occassion field is required."),
            },
            'sub_occassion': {
                'required': _("Sub Occassion field is required."),
            },
            'person_type': {
                'required': _("Person Type field is required."),
            },
        }


class ColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ['color']

        widgets = {
            'color': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Color'}),
        }

        error_messages = {
            'color': {
                'required': _("Color field is required."),
            },
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand']

        widgets = {
            'brand': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Brand'}),
        }

        error_messages = {
            'brand': {
                'required': _("Brand field is required."),
            },
        }


class GstCodesForm(forms.ModelForm):
    class Meta:
        model = GstCodes
        exclude = ['is_deleted','creator','updater','auto_id']

        widgets = {
            'type': Select(attrs={'class': 'select required  form-control', 'placeholder': 'TYPE'}, choices=TYPE),
            'code': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Code'}),
            'cgst_rate': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'CGST'}),
            'igst_rate': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'IGST'}),
            'sgst_rate': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'SGST'}),

        }

        error_messages = {

        }