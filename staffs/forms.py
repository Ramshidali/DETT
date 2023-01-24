from dal import autocomplete
from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput, CheckboxInput
from django.utils.translation import ugettext_lazy as _

from staffs.models import Designation, Staff


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']

        widgets = {
            'name': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Name'}),
        }

        error_messages = {
            'name': {
                'required': _("Unit Of Measurement field is required."),
            },
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted', 'user']

        widgets = {
            'designation': autocomplete.ModelSelect2(url='staffs:designation_autocomplete',
                                                     attrs={'data-placeholder': 'Designation',
                                                            'data-minimum-input-length': 1}, ),
            'name': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Name'}),
            'email': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Email'}),
            'phone': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Phone'}),
            'address': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Adrress'}),
            'bank_name': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Bank Name'}),
            'branch': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Branch'}),
            'bank_account_name': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Bank Name'}),
            'ifsc_code': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'IFSC'}),
            'account_number': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Account Number'}),

        }

        error_messages = {
            'designation': {
                'required': _("Designation field is required."),
            },
            'name': {
                'required': _("Name field is required."),
            },
            'phone': {
                'required': _("Phone field is required."),
            },
            'address': {
                'required': _("Address field is required."),
            },
            'bank_name': {
                'required': _("Bank Name field is required."),
            },
            'bank_account_name': {
                'required': _("Bank Account Name field is required."),
            },
            'ifsc_code': {
                'required': _("IFSC field is required."),
            },
            'account_number': {
                'required': _("Account Number field is required."),
            },
        }
