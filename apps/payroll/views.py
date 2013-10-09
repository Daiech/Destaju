# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.payroll.forms import *
from apps.payroll.models import *
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


@login_required()
def list_discounts_applied(request):
    """List all users with resume of discounts already applied"""    
    obj_list = DiscountsApplied.objects.get_user_with_discounts_applied()
    # for obj in obj_list:
    #     print "OBJETO", obj.discountsapplied_employee.all()
    show_modal = False
    return render_to_response('discounts_applied.html', locals(), context_instance=RequestContext(request))

def read_discounts_applied(request,id_user):
    """ Show all discounts for a user"""
    obj_list = DiscountsApplied.objects.get_user_with_discounts_applied()
    # for obj in obj_list:
    #     print "OBJETO", obj.discountsapplied_employee.all()
    user_obj = get_object_or_404(obj_list,pk=id_user)
    show_modal = True
    return render_to_response('read_user_discounts.html', locals(), context_instance=RequestContext(request))


def create_discount_applied(request, id_user):
    """Form to apply a general discount to an employee"""
    obj_list = DiscountsApplied.objects.get_user_with_discounts_applied()
    user_obj = get_object_or_404(User,pk=id_user)
    if request.method == 'POST':
        form  = DiscountsAppliedForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.admin = request.user
            obj.employee = user_obj
            obj.save()
            form = DiscountsAppliedForm()
            if not ('_createanother' in request.POST):
                return HttpResponseRedirect(reverse(read_discounts_applied, kwargs={'id_user': user_obj.pk}))
        else:
            show_modal = True
        if '_createanother' in request.POST:
            show_modal = True
    else:
        form  = DiscountsAppliedForm() 
        show_modal =True
    form_mode  = "_create"
    return render_to_response('create_discount_applied.html', locals(), context_instance=RequestContext(request))


def update_discount_applied(request,id_discount_applied):
    """Form to edit a general discount to an employee"""
    obj_list = DiscountsApplied.objects.get_user_with_discounts_applied()
    discount_obj = get_object_or_404(DiscountsApplied, pk= id_discount_applied)
    user_obj = discount_obj.employee
    if request.method == 'POST':
        form  = DiscountsAppliedForm(request.POST, instance=discount_obj)
        if form.is_valid():
            obj = form.save(commit=False)
#            obj.admin = request.user
#            obj.employee = user_obj
            obj.save()
            form = DiscountsAppliedForm()
            return HttpResponseRedirect(reverse(read_discounts_applied, kwargs={'id_user': user_obj.pk}))
        else:
            show_modal = True
    else:
        form  = DiscountsAppliedForm(instance=discount_obj) 
        show_modal =True
    form_mode  = "_update"
    return render_to_response('create_discount_applied.html', locals(), context_instance=RequestContext(request))


@login_required()
def delete_discount_applied(request, id_discount_applied):
    """Delete a discount applied"""
    obj = get_object_or_404(DiscountsApplied, pk=id_discount_applied)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(read_discounts_applied, kwargs={'id_user': obj.employee.pk}))













