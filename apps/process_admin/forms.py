#encoding:utf-8
from django import forms
from apps.process_admin.models import Activities, UserProfile, UserType, Employments, LegalDiscounts, GeneralDiscounts, Places, Tools
from apps.process_admin.validators import validate_dni
from django.contrib.auth.models import User


class ActivityForm(forms.ModelForm):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    measuring_unit = forms.CharField(label="Unidad de medida", widget=forms.TextInput(attrs={'placeholder': 'Unidad de medida'}))
    value = forms.CharField(label="Valor", widget=forms.TextInput(attrs={'placeholder': '','type':"number"}))
    is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = Activities
        fields = ('code','name', 'description', 'measuring_unit', 'value', 'is_available')

    
class UserProfileForm(forms.ModelForm):
    """docstring for UserProfileForm"""
    queryset_usertype = UserType.objects.exclude(pk=1).order_by('-pk').all()
    queryset_employments = Employments.objects.all()

    dni = forms.CharField(label="* Cédula", validators=[], widget=forms.TextInput(attrs={'placeholder': 'Cédula de ciudadanía', 'autofocus': 'autofocus'}))
    cell_phone = forms.CharField(label="* Celular", widget=forms.TextInput(attrs={'placeholder': 'Telefono Celular', 'type': 'tel'}))
    city = forms.CharField(label="* Ciudad", widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}))
    address = forms.CharField(label="* Dirección", widget=forms.TextInput(attrs={'placeholder': 'Dirección'}))
    date_born = forms.CharField(label="* Fecha de nacimiento", widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    is_active_worker = forms.BooleanField(label="* Trabajador activo", initial=True, required=False)
    user_type = forms.ModelChoiceField(label="* Tipo de usuario", queryset=queryset_usertype, empty_label=None)
    employment = forms.ModelChoiceField(label="Cargo", required=False, queryset=queryset_employments, empty_label="(Seleccione)")

    def is_dni_unique(self, user):
        cleaned_data = self.cleaned_data
        try:
            u = UserProfile.objects.exclude(user=user).get(dni=cleaned_data["dni"])
            print "UUUUUUUUUUUUUUUUU", u
            if u:
                from django.core.exceptions import ValidationError
                raise ValidationError('estas editandote, Pilas, alguien ya tiene esta cedula')
        except UserProfile.DoesNotExist, e:
            return True

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            user_obj = self.instance.pk
        except Exception, e:
            user_obj = None
            print "HOOOOO*//////////////////////////// %s" % e
        if user_obj:
            """if user_obj is defined: the form has an instance. (updating)"""
            there_is_dni = UserProfile.objects.exclude(user=self.instance.user).filter(dni=cleaned_data["dni"])
        else:
            """if user_obj is not defined: the form doesn't have an instance. (creating)"""
            there_is_dni = UserProfile.objects.filter(dni=cleaned_data["dni"])
        if there_is_dni:
            from django.core.exceptions import ValidationError
            raise ValidationError('Cédula duplicada, verifique que otro usuario no tenga esta misma cédula.')
        return cleaned_data

    class Meta:
        model = UserProfile
        fields = ('dni','cell_phone', 'city', 'address', 'date_born', 'is_active_worker', 'user_type', 'employment')
        

class LegalDiscountForm(forms.ModelForm):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    value = forms.CharField(label="Porcentaje", widget=forms.TextInput(attrs={'placeholder': '','type':"number"}))
    is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = LegalDiscounts
        fields = ('code','name', 'description', 'value', 'is_available')
        
        
class GeneralDiscountForm(forms.ModelForm):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = GeneralDiscounts
        fields = ('code','name', 'description', 'is_available')
         
        
class EmploymentsForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    
    class Meta:
        model = Employments
        fields = ('name', 'description')
        

class PlacesForm(forms.ModelForm):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = Places
        fields = ('code','name', 'description', 'is_available')
        

class ToolsForm(forms.ModelForm):
    code = forms.CharField(label="Codigo", widget=forms.TextInput(attrs={'placeholder': 'Codigo', 'autofocus': 'autofocus'}))
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'placeholder': 'Descripcion del anuncio'}))
    is_available = forms.BooleanField(label="Disponible", required=False, initial=True)
    
    class Meta:
        model = Tools
        fields = ('code','name', 'description', 'is_available')
