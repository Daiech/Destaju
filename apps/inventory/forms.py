#encoding:utf-8
from django import forms
from django.contrib.auth.models import User
from apps.production_orders.models import ProductionOrder
from apps.process_admin.models import Tools
from apps.inventory.models import QuantityProviderTool, ProviderOrder, QuantityEmployedTool, EmployedOrder, Inventory
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelFormSet

def user_unicode(self):
    try:
        dni = self.userprofile.dni
    except:
        dni = "Sin DNI"
    return  self.username if self.get_full_name() == ""  else u"%s - %s" % (dni, self.get_full_name())

User.__unicode__ = user_unicode


class ProviderOrderForm(forms.ModelForm):  
    queryset_user_provider = User.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk = 8)

    user_provider = forms.ModelChoiceField(label="Proveedor", queryset=queryset_user_provider, empty_label=None)
    invoice_number = forms.CharField(label=u"No. Factura", widget=forms.TextInput(attrs={'placeholder': u"# factura"}), required=False)
    details = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    class Meta:
        model = ProviderOrder
        fields = ('user_provider', 'invoice_number', 'details')


class QuantityProviderToolForm(forms.ModelForm):
    queryset_tools = Tools.objects.filter(is_active=True, is_available=True) 

    tool = forms.ModelChoiceField(label="Items", queryset=queryset_tools)
    quantity = forms.CharField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))
    unit_value = forms.CharField(label="Valor unidad", widget=forms.TextInput(attrs={'placeholder': 'Valor unidad','type':"number","step":"any"}))

    class Meta:
        model = QuantityProviderTool
        fields = ('tool', 'quantity', 'unit_value')

    def clean_quantity(self):
        if float(self.cleaned_data.get('quantity')) <= 0:
            raise forms.ValidationError(u"El número de items debe ser mayor que 0 ")
        return self.cleaned_data.get('quantity')

    def clean_unit_value(self):
        if float(self.cleaned_data.get('unit_value')) <= 0:
            raise forms.ValidationError(u"El número de items debe ser mayor que 0 ")
        return self.cleaned_data.get('unit_value')


############## --------------------------------    Employed ---------------------------------------------------###########################

class EmployedOrderForm(forms.ModelForm):  
    TYPE_ORDER = (('','---------'),('Recovery','Devolucion'),('Output_Stock',"Salida"))
    list_production_order = ProductionOrder.objects.get_all_active().values_list('pk', flat=True)[0:50] # .filter(status=1)
    

    production_order = forms.ModelChoiceField(label="Orden de produccion", queryset=ProductionOrder.objects.filter(pk__in=list_production_order).order_by('-date_added') )  #, empty_label=None
    type_order = forms.ChoiceField(label="Tipo", choices=TYPE_ORDER)
    details = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    class Meta:
        model = EmployedOrder
        fields = ('production_order','type_order','details')

    



class QuantityEmployedToolForm(forms.ModelForm):
    queryset_tools = Tools.objects.filter(is_active=True, is_available=True) 
    # colocar solo las herramientas que esten disponibles en el almacen

    tool = forms.ModelChoiceField(label="Items", queryset=queryset_tools)
    quantity = forms.CharField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))

    class Meta:
        model = QuantityEmployedTool
        fields = ('tool', 'quantity')

    def add_employed_order(self,employed_order):
        self.instance.employed_order = employed_order

    def clean_quantity(self):
        if self.instance.employed_order.type_order == "Output_Stock" or self.instance.employed_order.type_order == "Output":
            try:
                inventory_obj = Inventory.objects.get(tool=self.cleaned_data.get('tool'))
            except:
                raise forms.ValidationError("Esta herramienta no se encuentra disponible en el inventario")
            if inventory_obj.quantity < float(self.cleaned_data.get('quantity')):
                raise forms.ValidationError("No hay suficientes items disponibles en el inventario, disponible ( %s: %s )"%(inventory_obj.tool.name, inventory_obj.quantity ))
        if float(self.cleaned_data.get('quantity')) <= 0:
            raise forms.ValidationError(u"El número de items debe ser mayor que 0 ")
        return self.cleaned_data.get('quantity')

