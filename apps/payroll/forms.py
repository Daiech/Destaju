#encoding:utf-8
from django import forms
# from apps.process_admin.models import LegalDiscounts, GeneralDiscounts
from apps.payroll.models import DiscountsApplied
from django.contrib.auth.models import User


class DiscountsAppliedForm(forms.ModelForm):
    # code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    # name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    # description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    # measuring_unit = forms.CharField(label="Unidad de medida", widget=forms.TextInput(attrs={'placeholder': 'Unidad de medida'}))
    # value = forms.CharField(label="Valor", widget=forms.TextInput(attrs={'placeholder': '','type':"number","step":"any"}))
    # is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = Activities
        fields = ('general_discount', 'value')