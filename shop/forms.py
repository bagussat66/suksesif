from django import forms
from django.db.models.fields import CharField
from django.forms.widgets import TextInput
# from django_address.models


PAYMENT_CHOICES = (
    ('Q','QRIS'),
    ('M','Bank Mandiri'),
    ('B','Bank Central Asia'),
    ('C','Visa/Mastercard')
)

class CheckoutForm(forms.Form):
    address = forms.CharField(label="Alamat",widget=forms.TextInput(attrs={
        'placeholder':'Jl. Sudirman No. 1'}
    ))

    zip_code = forms.CharField(label="Kode Pos",widget=forms.TextInput(attrs={
        'placeholder':'00000'
    }))

    save_address = forms.BooleanField(label="Simpan Alamat?",required=False,widget=forms.CheckboxInput())
    save_info = forms.BooleanField(label="Simpan Informasi Pembayaran?",required=False,widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(label="Informasi Pembayaran",widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
