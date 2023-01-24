from customers.models import CustomerAddress
from rest_framework import serializers



class AddressSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerAddress
        fields = ['name','address_line1','phone','pincode','street','city','landmark','state','address_type','is_default']