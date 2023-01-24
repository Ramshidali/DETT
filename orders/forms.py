from dal import autocomplete
from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput, CheckboxInput
from django.utils.translation import ugettext_lazy as _

from orders.models import Order
from products.models import GstCodes

class OrderChargesForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courier_service_charge','sac_code']

        widgets = {
            'courier_service_charge': TextInput(attrs={'class': 'required  form-control', 'placeholder': 'Courier Service Charge'}),
            'sac_code': autocomplete.ModelSelect2(url='products:hsn_autocomplete', attrs={'data-placeholder': 'Enter SAC Code', 'data-minimum-input-length': 1}, ),
        }

        error_messages = {

        }