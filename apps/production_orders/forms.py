#encoding:utf-8
from django import forms
from apps.production_orders.models import ProductionOrder, FillingProOrd, QualificationProOrd, Filling #Qualifications
from apps.process_admin.models import Activities, Places, Tools, UserProfile
from django.contrib.auth.models import User


def user_unicode(self):
    try:
        dni = self.userprofile.dni
    except:
        dni = "Sin DNI"
    return  self.username if self.get_full_name() != ""  else u"%s - %s" % (dni, self.get_full_name())

User.__unicode__ = user_unicode


class ProductionOrderForm(forms.ModelForm):
    queryset_activity = Activities.objects.filter(is_active=True,is_available=True)
    queryset_place = Places.objects.filter(is_active=True, is_available=True)
    queryset_responsable = User.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk = 7)
    queryset_tools = Tools.objects.filter(is_active=True, is_available=True) 
    
    activity = forms.ModelChoiceField(label="Actividad", queryset=queryset_activity, empty_label=None)
    place = forms.ModelChoiceField(label="Lugar", queryset=queryset_place, empty_label=None)
    responsible = forms.ModelMultipleChoiceField(label="Responsables", queryset=queryset_responsable,  widget= forms.SelectMultiple(attrs={'class': 'chosen-select', 'data-placeholder':"Selecciona los responsables"}))
    tools = forms.ModelMultipleChoiceField(label="Herramientas", queryset=queryset_tools, required=False, widget= forms.SelectMultiple(attrs={'class': 'chosen-select', 'data-placeholder':"Selecciona las herramientas"}))
    comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    class Meta:
        model = ProductionOrder
        fields = ('activity', 'place', 'responsible', 'tools', 'comments')


class FillingForm(forms.ModelForm):
    value = forms.CharField(label="Value", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))
    comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    class Meta:
        model = Filling
        fields = ('user', 'value', 'comments')
        widgets = {
            'user': forms.Select(attrs={'class':'name-only'}),
        }


class FillingProOrdForm(forms.ModelForm):
    comments = forms.CharField(label=u"Observaciónes Generales", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes Generales"}), required=False)
    class Meta:
        model = Filling
        fields = ('comments',)
#        widgets = {
#            'user': forms.Select(attrs={'class':'name-only'}),
#        }

class QualificationsForm(forms.ModelForm):
    comments = forms.CharField(label=u"Observaciónes", widget=forms.TextInput(attrs={'placeholder': u"Observaciónes"}), required=False)

    class Meta:
        model = QualificationProOrd
        fields = ('value', 'status', 'comments')
        

class ListProductionOrderForm(forms.Form):
    date_from = forms.DateTimeField(label="Desde", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d'])
    date_to = forms.DateTimeField(label="Hasta", widget=forms.widgets.DateTimeInput(attrs={'class': 'date-pick'}), input_formats=['%Y-%m-%d'])
    type_date = forms.ChoiceField(label="Fecha",choices=[('added',u"Creación"),('modified',u"Modificación")])
