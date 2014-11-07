#encoding:utf-8
from django import forms
from django.contrib.auth.models import User
# from apps.production_orders.models import ProductionOrder, FillingProOrd, QualificationProOrd, Filling #Qualifications
from apps.process_admin.models import Tools
from apps.inventory.models import QuantityProviderTool, ProviderOrder 

def user_unicode(self):
    try:
        dni = self.userprofile.dni
    except:
        dni = "Sin DNI"
    return  self.username if self.get_full_name() == ""  else u"%s - %s" % (dni, self.get_full_name())

User.__unicode__ = user_unicode


class ProviderOrderForm(forms.ModelForm):
    # queryset_activity = Activities.objects.filter(is_active=True,is_available=True)
    # queryset_place = Places.objects.filter(is_active=True, is_available=True)
    # queryset_responsable = User.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk = 7)
    
    
    queryset_user_provider = User.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk = 8)

    # activity = forms.ModelChoiceField(label="Actividad", queryset=queryset_activity, empty_label=None)
    # place = forms.ModelChoiceField(label="Lugar", queryset=queryset_place, empty_label=None)
    # responsible = forms.ModelMultipleChoiceField(label="Responsables", queryset=queryset_responsable,  widget= forms.SelectMultiple(attrs={'class': 'chosen-select', 'data-placeholder':"Selecciona los responsables"}))
    # tools = forms.ModelMultipleChoiceField(label="Herramientas", queryset=queryset_tools, required=False, widget= forms.SelectMultiple(attrs={'class': 'chosen-select', 'data-placeholder':"Selecciona las herramientas"}))
    # comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)


    # user_generator = models.ForeignKey(User, related_name='%(class)s_user_generator') 
    user_provider = forms.ModelChoiceField(label="Proveedor", queryset=queryset_user_provider, empty_label=None)
    # user_approver = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_approved') 
    invoice_number = forms.CharField(label=u"No. Factura", widget=forms.TextInput(attrs={'placeholder': u"# factura"}), required=False)
    details = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)
    # status_order = models.CharField(max_length=20, choices=STATUS_CHOICES,  default='Waiting')
    # date_approved = models.DateTimeField(null=True, blank=True)

    class Meta:
        model = ProviderOrder
        fields = ('user_provider', 'invoice_number', 'details')


class QuantityProviderToolForm(forms.ModelForm):
    # value = forms.CharField(label="Value", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))
    # comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    queryset_tools = Tools.objects.filter(is_active=True, is_available=True) 

    tool = forms.ModelChoiceField(label="Items", queryset=queryset_tools, empty_label=None)
    quantity = forms.CharField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))
    unit_value = forms.CharField(label="Valor unidad", widget=forms.TextInput(attrs={'placeholder': 'Valor unidad','type':"number","step":"any"}))
    # provider_order = models.ForeignKey(ProviderOrder, null=True, blank=True, related_name='%(class)s_provider_order') 

    class Meta:
        model = QuantityProviderTool
        fields = ('tool', 'quantity', 'unit_value')
        # widgets = {
        #     'user': forms.Select(attrs={'class':'name-only'}),
        # }


# class FillingProOrdForm(forms.ModelForm):
#     comments = forms.CharField(label=u"Observaciónes Generales", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes Generales"}), required=False)
#     class Meta:
#         model = Filling
#         fields = ('comments',)
# #        widgets = {
# #            'user': forms.Select(attrs={'class':'name-only'}),
# #        }

# class QualificationsForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(QualificationsForm, self).__init__(*args, **kwargs)

#         # self.fields['status'].label = "Estado"
#         self.fields['value'].label = "Valor"
        
#     comments_value = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

#     class Meta:
#         model = QualificationProOrd
#         fields = ('value', 'comments_value')

# class ApprovalForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ApprovalForm, self).__init__(*args, **kwargs)

#         self.fields['status'].label = "Estado"
#         # self.fields['value'].label = "Valor"
        
#     comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

#     class Meta:
#         model = QualificationProOrd
#         fields = ('status', 'comments')
        

# class ListProductionOrderForm(forms.Form):
#     TYPE_CHOICES=[
#                   ('added',u"Creación"),
#                   ('modified',u"Modificación"),
#                   ('filling',u"LLenado")
#                   ]
    
#     date_from = forms.DateTimeField(label="Desde", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d'])
#     date_to = forms.DateTimeField(label="Hasta", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d'])
#     type_date = forms.ChoiceField(label="Fecha",choices=TYPE_CHOICES)
