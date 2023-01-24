# django
from django.forms.widgets import TextInput, Textarea, Select
from django import forms

from customers.models import CustomerAddress


class CustomerAddressForm(forms.ModelForm):

    class Meta:
        model = CustomerAddress
        fields = ['name', 'address_line1', 'phone',
                  'pincode', 'street', 'city', 'state', 'landmark']

        widgets = {
            'name': TextInput(attrs={'name': 'name', 'placeholder': 'Name'}),
            'phone': TextInput(attrs={'name': 'name', 'placeholder': 'phone'}),
            'pincode': TextInput(attrs={'name': 'mobile-number', 'placeholder': 'pincode'}),
            'street': TextInput(attrs={'name': 'street', 'placeholder': 'street', 'class': 'address-street'}),
            'city': TextInput(attrs={'name': 'city', 'placeholder': 'city'}),
            'landmark': TextInput(attrs={'name': 'landmark', 'placeholder': 'landmark'}),
            'state': TextInput(attrs={'name': 'state', 'placeholder': 'State'}),
            'address_line1': Textarea(attrs={'name': 'address', 'placeholder': 'Address Line1'}),
        }
