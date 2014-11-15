#encoding:utf-8
from django import forms
from django.contrib.auth.models import User
from apps.production_orders.models import ProductionOrder
from apps.process_admin.models import Tools
from apps.inventory.models import QuantityProviderTool, ProviderOrder, QuantityEmployedTool, EmployedOrder

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


############## --------------------------------    Employed ---------------------------------------------------###########################

class EmployedOrderForm(forms.ModelForm):  
    TYPE_ORDER = (('Recovery','Devolucion'),('Output_Stock',"Salida"))
    queryset_production_order = ProductionOrder.objects.get_all_active().values_list('pk', flat=True)[0:50] # .filter(status=1)

    production_order = forms.ModelChoiceField(label="Orden de produccion", queryset=ProductionOrder.objects.filter(pk__in=list(queryset_production_order)).order_by('-date_added') )  #, empty_label=None
    type_order = forms.CharField(label="Tipo", widget=forms.Select(choices=TYPE_ORDER))
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

