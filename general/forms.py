from dal import autocomplete
from django import forms
from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput
from django.utils.translation import ugettext_lazy as _

from general.models import Occassion, SubOccassion, SetCoupon, PersonType, SetDueDays, Phone, GiftImage, Extras, Slider


class OccassionForm(forms.ModelForm):
    class Meta:
        model = Occassion
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'occassion': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Occassion'}),
            'occassion_image': FileInput()
        }

        error_messages = {
            'occassion': {
                'required': _("Ocassion field is required."),
            },
            'occassion_image': {
                'required': _("Image field is required."),
            },
        }


class SubOccassionForm(forms.ModelForm):
    class Meta:
        model = SubOccassion
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'occassion': autocomplete.ModelSelect2(url='general:occassion_autocomplete',
                                                   attrs={'data-placeholder': 'Choose Occassion',
                                                          'data-minimum-input-length': 1}, ),
            'sub_occassion_image': FileInput(),
            'sub_occassion': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Sub Occassion'}),

        }

        error_messages = {
            'occassion': {
                'required': _("Ocassion field is required."),
            },
            'sub_occassion_image': {
                'required': _("Image field is required."),
            },
            'sub_occassion': {
                'required': _("Sub Occassion field is required."),
            },
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = SetCoupon
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'coupon_code': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Copon dode'}),
            'offer_percentage': TextInput(attrs={'class': 'required form-control', 'placeholder': 'percentage'}),
            'title': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Title'}),
            'description': TextInput(attrs={'class': 'required form-control', 'placeholder': 'description'}),

        }

        error_messages = {
            'coupon_code': {
                'required': _("Coupon Code field is required."),
            },
            'offer_percentage': {
                'required': _("Offer Percentage field is required."),
            },
            'description': {
                'required': _("description field is required."),
            },
            'title': {
                'required': _("Title field is required."),
            }
        }


class PersonTypeForm(forms.ModelForm):
    class Meta:
        model = PersonType
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'person_type': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Person Type'}),
        }

        error_messages = {
            'person_type': {
                'required': _("Person Type field is required."),
            },
        }


class DueDaysForm(forms.ModelForm):
    class Meta:
        model = SetDueDays
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'no_of_days': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'No of days'}),
        }

        error_messages = {
            'no_of_days': {
                'required': _("NO of days Type field is required."),
            },
        }


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone']

        widgets = {
            'phone': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Phone'}),
        }

        error_messages = {
            'phone': {
                'required': _("Phone field is required."),
            },
        }


class GiftImageForm(forms.ModelForm):
    class Meta:
        model = GiftImage
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'image': FileInput(),
        }

        error_messages = {
            'image': {
                'required': _("Image field is required."),
            },
        }


class ExtrasForm(forms.ModelForm):
    class Meta:
        model = Extras
        fields = '__all__'

        widgets = {
            'inter_state_charges': TextInput(
                attrs={'class': 'required  form-control', 'placeholder': 'Inter state Charges'}),
            'intra_state_charges': TextInput(
                attrs={'class': 'required  form-control', 'placeholder': 'Intra state Charges'}),
            'special_discount': TextInput(
                attrs={'class': 'required  form-control', 'placeholder': 'Specia Discount (%)'}),

        }

        error_messages = {
            'inter_state_charges': {
                'required': _("Inter state field is required."),
            },
            'intra_state_charges': {
                'required': _("Intra state field is required."),
            },
            'special_discount': {
                'required': _("Special Discount state field is required."),
            },
        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'title': TextInput(
                attrs={'class': 'required  form-control', 'placeholder': 'Title'}),
            'image': FileInput(),
        }

        error_messages = {
            'image': {
                'required': _("Image field is required."),
            },
            'title': {
                'required': _("Title field is required."),
            },
        }
