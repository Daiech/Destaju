# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.payroll.forms import *
from apps.payroll.models import *
from apps.production_orders.models import Filling
from apps.process_admin.models import LegalDiscounts
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
#from django.db.models import Sum


@login_required()
def list_discounts_applied(request):
    """List all users with resume of discounts already applied"""    
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True)
    show_modal = False
    return render_to_response('discounts_applied.html', locals(), context_instance=RequestContext(request))

def read_discounts_applied(request,id_user):
    """ Show all discounts for a user"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True)
    user_obj = get_object_or_404(obj_list,pk=id_user)
    show_modal = True
    return render_to_response('read_user_discounts.html', locals(), context_instance=RequestContext(request))


def create_discount_applied(request, id_user):
    """Form to apply a general discount to an employee"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True)
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
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True)
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


@login_required()
def list_payroll(request):
    """Show the list of employees with values of activities, general discounts applied and legal discounts applied."""
    payroll_list =[]
    obj_list = MyUser.objects.filter(userprofile__user_type__pk__in=[7,8])
    filling_list = Filling.objects.filter()
    filling_list2 = Filling.objects.filter().aggregate(total = Sum('value'))
    discounts_list = DiscountsApplied.objects.filter(is_active=True)
    legal_discounts = LegalDiscounts.objects.filter(is_active=True)
    global_payroll = 0
    for obj in obj_list:
        activities = filling_list.filter(user=obj)
        discounts = discounts_list.filter(employee=obj)
        total_activities = 0
        total_discounts = discounts.aggregate(t= Sum('value'))
        total_discounts = total_discounts["t"] if total_discounts["t"] != None else 0
        for a in activities:
            total_activities +=  (int(a.value) * int(a.filling_pro_ord.production_order.activity.value))
        total_payroll = total_activities-total_discounts
        global_payroll += total_payroll
        payroll_list.append({"user":obj,
                             "activities":activities,
                             "total_activities": total_activities,
                             "discounts": discounts,
                             "total_discounts": total_discounts,
                             "total_payroll": total_payroll
                             })
    
    return render_to_response('payroll.html', locals(), context_instance=RequestContext(request))








