#encoding:utf-8
from django import forms

class ActivityForm(forms.Form):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    measuring_unit = forms.CharField(label="Unidad de medida", widget=forms.TextInput(attrs={'placeholder': 'Unidad de medida'}))
    value = forms.CharField(label="Precio", widget=forms.TextInput(attrs={'placeholder': ''}))