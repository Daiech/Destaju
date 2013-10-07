# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
from apps.production_orders.forms import *
from apps.production_orders.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#from django.core import serializers
#from apps.actions_log.views import save_with_modifications
# from apps.process_admin.models import Tools, Places, Activities
# from apps.actions_log.views import save_with_modifications
# from django.forms.formsets import modelformset_factory
# from django.forms.models import modelformset_factory
from apps.account.decorators import access_required
from django.db.models import Max, Sum

@login_required()
def read_discounts_applied(request):
    """Read discounts already applied"""    
    obj_list = User.objects.filter(is_active=True) \
    .annotate(total_discounts = Sum('discountsapplied_employee__value'))
    # for obj in obj_list:
    #     print "OBJETO", obj.discountsapplied_employee.all()
    return render_to_response('discounts_applied.html', locals(), context_instance=RequestContext(request))


def create_discount_applied(request):
    """Form to add a general discount to an employee"""
    if request.method == 'POST':
        form  = DiscountsAppliedForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            form = DiscountsAppliedForm()
        else:
                show_form = True
        if '_createanother' in request.POST:
            show_form = True
    else:
        form  = DiscountsAppliedForm() 
    return render_to_response('discounts_applied.html', locals(), context_instance=RequestContext(request))


def update_discount_applied(request):
    pass


def delete_discount_applied(request):
    pass