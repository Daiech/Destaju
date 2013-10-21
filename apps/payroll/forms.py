# encoding:utf-8
from django import forms
# from apps.process_admin.models import LegalDiscounts, GeneralDiscounts
from apps.payroll.models import DiscountsApplied, IncreasesApplied
from django.contrib.auth.models import User


class DiscountsAppliedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DiscountsAppliedForm, self).__init__(*args, **kwargs)

        self.fields['general_discount'].label = "Tipo de descuento"
        self.fields['value'].label = "Valor"

    class Meta:
        model = DiscountsApplied
        fields = ('general_discount', 'value')


class IncreasesAppliedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IncreasesAppliedForm, self).__init__(*args, **kwargs)

        self.fields['increase'].label = "Tipo de aumento"
        self.fields['value'].label = "Valor"

    class Meta:
        model = IncreasesApplied
        fields = ('increase', 'value')
        
