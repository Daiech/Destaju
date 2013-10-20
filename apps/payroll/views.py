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
@access_required("superadmin", "admin")
def list_discounts_applied(request):
    """List all users with resume of discounts already applied"""    
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    show_modal = False
    return render_to_response('discounts_applied.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def read_discounts_applied(request,id_user):
    """ Show all discounts for a user"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    user_obj = get_object_or_404(obj_list,pk=id_user)
    show_modal = True
    return render_to_response('read_user_discounts.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def create_discount_applied(request, id_user):
    """Form to apply a general discount to an employee"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    user_obj = get_object_or_404(obj_list,pk=id_user)
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


@login_required()
@access_required("superadmin", "admin")
def update_discount_applied(request,id_discount_applied):
    """Form to edit a general discount to an employee"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    discount_obj = get_object_or_404(DiscountsApplied, pk= id_discount_applied)
    user_obj = discount_obj.employee
    if request.method == 'POST':
        form  = DiscountsAppliedForm(request.POST, instance=discount_obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.admin = request.user
            # obj.employee = user_obj
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


@access_required("superadmin", "admin")
@login_required()
def delete_discount_applied(request, id_discount_applied):
    """Delete a discount applied"""
    obj = get_object_or_404(DiscountsApplied, pk=id_discount_applied)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(read_discounts_applied, kwargs={'id_user': obj.employee.pk}))


@login_required()
@access_required("superadmin", "admin")
def list_payroll(request):
    """Show the list of employees with values of activities, general discounts applied and legal discounts applied."""
    payroll_list =[]
    obj_list = MyUser.objects.filter(userprofile__user_type__pk__in=[7,8])
    filling_list = Filling.objects.filter()
    filling_list2 = Filling.objects.filter().aggregate(total=Sum('value'))
    discounts_list = DiscountsApplied.objects.filter(is_active=True)
    legal_discounts = LegalDiscounts.objects.filter(is_active=True)
    global_payroll = 0
    for obj in obj_list:
        #total activities
        activities = filling_list.filter(user=obj, filling_pro_ord__production_order__status=3)
        total_activities = 0
        for a in activities:
            a1 = int(a.filling_pro_ord.production_order.activity.value)
            activity_value = int(a.value) *  a1
            total_activities +=  activity_value
        total_payroll=total_activities

        #adjust
        SMMLV = 660000
        adjust = 0
        if total_activities < SMMLV:
            adjust = SMMLV-total_activities
            total_payroll = total_payroll + adjust

        #legal discount
        if total_activities > (SMMLV*4):
            ld = LegalDiscounts.objects.get(pk=2)
        else:
            ld = LegalDiscounts.objects.get(pk=1)
        ld_value = (total_payroll/100)*int(ld.value)
        total_payroll = total_payroll-(total_payroll/100)*int(ld.value)

        #General discount
        discounts = discounts_list.filter(employee=obj)
        total_discounts = discounts.aggregate(t= Sum('value'))
        total_discounts = total_discounts["t"] if total_discounts["t"] != None else 0
        total_payroll = total_payroll-total_discounts
        
        global_payroll += total_payroll
        payroll_list.append({"user": obj,
                             "activities": activities,
                             "total_activities": total_activities,
                             "discounts": discounts,
                             "total_discounts": total_discounts,
                             "total_payroll": total_payroll,
                             "legal_discount_type": "%s %s%%"%(ld.name, ld.value),
                             "legal_discount_value": ld_value,
                             "adjust": adjust
                             })
    
    return render_to_response('payroll.html', locals(), context_instance=RequestContext(request))
