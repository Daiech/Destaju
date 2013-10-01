#encoding:utf-8
from django import forms
from apps.production_orders.models import ProductionOrder, FillingProOrd, QualificationProOrd, Filling, Qualifications
from apps.process_admin.models import Activities, Places, Tools, UserProfile
from django.contrib.auth.models import User


class ProductionOrderForm(forms.ModelForm):
    queryset_activity = Activities.objects.filter(is_active=True,is_available=True)
    queryset_place = Places.objects.filter(is_active=True, is_available=True)
    queryset_responsable = User.objects.filter(userprofile__is_active_worker=True)
    queryset_tools = Tools.objects.filter(is_active=True, is_available=True)
    
    activity = forms.ModelChoiceField(label="Actividad", queryset=queryset_activity, empty_label=None)
    place = forms.ModelChoiceField(label="Lugar", queryset=queryset_place, empty_label=None)
    responsible = forms.ModelChoiceField(label="Responsables", queryset=queryset_responsable, empty_label=None)
    tools = forms.ModelChoiceField(label="Herramientas", queryset=queryset_tools, empty_label="(Ninguna)")

    class Meta:
        model = ProductionOrder
        fields = ('activity', 'place', 'responsible', 'tools')