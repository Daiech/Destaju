#encoding:utf-8
from django import forms
from apps.process_admin.models import Activities
from django.forms import ModelForm

class ActivityForm(ModelForm):
    
    class Meta:
        model = Activities
        fields = ['code','name', 'description', 'measuring_unit', 'value', 'is_available']
        labels = {
            'code':'C&oacute;digo',
            'name':'Nombre',
            'description':'Descripci&oacute;n',
            'measuring_unit':'Unidad de medida',
            'value':'Precio',
            'is_available':'Disponible',
        }
    
    
    
#    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
#    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
#    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
#    measuring_unit = forms.CharField(label="Unidad de medida", widget=forms.TextInput(attrs={'placeholder': 'Unidad de medida'}))
#    value = forms.CharField(label="Precio", widget=forms.TextInput(attrs={'placeholder': ''}))