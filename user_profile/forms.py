from django import forms
from django.db.models.fields import CharField
from django.forms.widgets import TextInput

from .models import Address

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address',
            'zip_code'
        ]
    
    def clean_title(self,*args,**kwargs):
        address = self.cleaned_data.get("address")
        if not "J" in address:
            raise forms.ValidationError("Bukan alamat yang valid.")
        return address
