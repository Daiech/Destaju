#encoding:utf-8
from django import forms
from apps.production_orders.models import ProductionOrder, FillingProOrd, QualificationProOrd, Filling, Qualifications
from apps.process_admin.models import Activities, Places, Tools, UserProfile
from django.contrib.auth.models import User


def user_unicode(self):
    return  u'%s' % (self.get_full_name())

User.__unicode__ = user_unicode


class ProductionOrderForm(forms.ModelForm):
    queryset_activity = Activities.objects.filter(is_active=True,is_available=True)
    queryset_place = Places.objects.filter(is_active=True, is_available=True)
    queryset_responsable = User.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk = 7)
    queryset_tools = Tools.objects.filter(is_active=True, is_available=True) 
    
    activity = forms.ModelChoiceField(label="Actividad", queryset=queryset_activity, empty_label=None)
    place = forms.ModelChoiceField(label="Lugar", queryset=queryset_place, empty_label=None)
    responsible = forms.ModelMultipleChoiceField(label="Responsables", queryset=queryset_responsable)
    tools = forms.ModelMultipleChoiceField(label="Herramientas", queryset=queryset_tools, required=False)

    class Meta:
        model = ProductionOrder
        fields = ('activity', 'place', 'responsible', 'tools')


class FillingForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(FillingForm, self).__init__(*args, **kwargs)
    #     self.fields['value'].label = self.instance.user.username

    def __init__(self, *args, **kwargs):
        super(FillingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].widget.attrs['readonly'] = True
            self.fields['user'].widget.attrs['disabled'] = True

    def clean_user(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.user
        else:
            return self.cleaned_data['user']

    value = forms.CharField(label="Value", widget=forms.TextInput(attrs={'placeholder': 'cantidad','type':"number","step":"any"}))

    class Meta:
        model = Filling
        fields = ('user','value')
        widgets = {
            'user': forms.Select(attrs={'class':'name-only'}),
        }