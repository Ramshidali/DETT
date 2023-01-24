from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput
from django.utils.translation import ugettext_lazy as _

from delivery_agents.models import DeliveryAgent

# iterable
GENDER = (
    ("10", "Male"),
    ("20", "Female"),
    ("30", "Other"),
)


class AgentForm(forms.ModelForm):
    class Meta:
        model = DeliveryAgent
        exclude = ['id', 'date_added', 'is_deleted', 'user']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
            'email': TextInput(attrs={'class': 'required email form-control', 'placeholder': 'Email'}),
            'joining_date': TextInput(attrs={'class': 'required date-picker form-control', 'placeholder': 'Date'}),
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Phone'}),
            'address': Textarea(attrs={'class': 'required form-control', 'placeholder': 'Address'}),
            'gender': Select(choices=GENDER),
            'salary': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Salary'}),
            'location': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Location'}),
        }

        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'email': {
                'required': _("Email field is required."),
            },
        }
