# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.payroll.forms import *
from apps.payroll.models import *
from apps.production_orders.models import Filling, ProductionOrder
from apps.process_admin.models import LegalDiscounts
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from apps.account.decorators import access_required
from django.utils import simplejson as json


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
    discounts = user_obj.discountsapplied_employee.filter(is_active=True)
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
def list_increases_applied(request):
    """List all users with resume of increases already applied"""    
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    show_modal = False
    return render_to_response('increases_applied.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def read_increases_applied(request,id_user):
    """ Show all increases for a user"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    user_obj = get_object_or_404(obj_list,pk=id_user)
    show_modal = True
    increases = user_obj.increasesapplied_employee.filter(is_active=True)
    return render_to_response('read_user_increases.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def create_increase_applied(request, id_user):
    """Form to apply a general increase to an employee"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    user_obj = get_object_or_404(obj_list,pk=id_user)
    if request.method == 'POST':
        form  = IncreasesAppliedForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.admin = request.user
            obj.employee = user_obj
            obj.save()
            form = IncreasesAppliedForm()
            if not ('_createanother' in request.POST):
                return HttpResponseRedirect(reverse(read_increases_applied, kwargs={'id_user': user_obj.pk}))
        else:
            show_modal = True
        if '_createanother' in request.POST:
            show_modal = True
    else:
        form  = IncreasesAppliedForm() 
        show_modal =True
    form_mode  = "_create"
    return render_to_response('create_increase_applied.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def update_increase_applied(request,id_increase_applied):
    """Form to edit a general increase to an employee"""
    obj_list = MyUser.objects.filter(userprofile__is_active_worker=True, userprofile__user_type__pk=7)
    increase_obj = get_object_or_404(IncreasesApplied, pk= id_increase_applied)
    user_obj = increase_obj.employee
    if request.method == 'POST':
        form  = IncreasesAppliedForm(request.POST, instance=increase_obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.admin = request.user
            # obj.employee = user_obj
            obj.save()
            form = IncreasesAppliedForm()
            return HttpResponseRedirect(reverse(read_increases_applied, kwargs={'id_user': user_obj.pk}))
        else:
            show_modal = True
    else:
        form  = IncreasesAppliedForm(instance=increase_obj) 
        show_modal =True
    form_mode  = "_update"
    return render_to_response('create_increase_applied.html', locals(), context_instance=RequestContext(request))


@access_required("superadmin", "admin")
@login_required()
def delete_increase_applied(request, id_increase_applied):
    """Delete a increase applied"""
    obj = get_object_or_404(IncreasesApplied, pk=id_increase_applied)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(read_increases_applied, kwargs={'id_user': obj.employee.pk}))



@login_required()
@access_required("superadmin", "admin")
def list_payroll(request):
    """Show the list of employees with values of activities, general discounts applied and legal discounts applied."""
    payroll_list =[]

    obj_list = MyUser.objects.filter(userprofile__user_type__pk__in=[7,8])

    filling_list = Filling.objects.filter()
    filling_list2 = Filling.objects.filter().aggregate(total=Sum('value'))

    discounts_list = DiscountsApplied.objects.filter(is_active=True)
    increases_list = IncreasesApplied.objects.filter(is_active=True)

    legal_discounts = LegalDiscounts.objects.filter(is_active=True)

    global_payroll = 0
    for obj in obj_list:
        total_payroll = 0
        #total activities
        activities = filling_list.filter(user=obj, filling_pro_ord__production_order__qualificationproord__status=1).exclude(filling_pro_ord__production_order__status=4)
        total_activities = 0
        for a in activities:
            a1 = int(a.filling_pro_ord.production_order.activity.value)
            activity_value = int(a.value) *  a1
            total_activities +=  activity_value
        # total_payroll=total_activities

        #aumentos
        increases = increases_list.filter(employee=obj)
        total_increases = increases.aggregate(t= Sum('value'))
        total_increases_value = total_increases["t"] if total_increases["t"] != None else 0
        # total_payroll = total_payroll+total_increases_value

        total_accrued = total_activities + total_increases_value

        legal_discount_value = (total_accrued/100)*int(8)
        # total_payroll = total_accrued-legal_discount_value

        #General discount
        discounts = discounts_list.filter(employee=obj)
        total_discounts = discounts.aggregate(t= Sum('value'))
        total_discounts_value = total_discounts["t"] if total_discounts["t"] != None else 0

        total_payroll = total_accrued-total_discounts_value-legal_discount_value
        
        global_payroll += total_payroll

        #payroll
        payroll_list.append({"user": obj,
                             "activities": activities,
                             "total_activities": total_activities,
                             "discounts": discounts,
                             "total_discounts": total_discounts_value,
                             "increases": increases,
                             "total_increases": total_increases_value,
                             "total_payroll": total_payroll,
                             "legal_discount_type": "Seguridad social 8%",  #"%s %s%%"%(ld.name, ld.value),
                             "legal_discount_value": legal_discount_value,
                             "total_accrued": total_accrued
                             #"adjust": adjust
                             })
    last_payroll=False
    return render_to_response('payroll.html', locals(), context_instance=RequestContext(request))


@login_required()
def pdf_payroll_list(request):
    from os import listdir
    path = settings.MEDIA_ROOT + "/pdf/"
    obj_list = listdir(path)   
    pdf_url = settings.MEDIA_URL + "pdf/"
    return render_to_response('pdf_payroll_list.html', locals(), context_instance=RequestContext(request))


@login_required()
def set_payroll(request):
    if request.is_ajax():
        if request.method == "GET":
            payroll_obj = Payroll(admin = request.user)
            payroll_obj.save()
            ProductionOrder.objects.filter(status=3).update(status=4, payroll=payroll_obj)
            DiscountsApplied.objects.filter(is_active=True).update(is_active=False, payroll=payroll_obj)
            IncreasesApplied.objects.filter(is_active=True).update(is_active=False, payroll=payroll_obj)
            json_str = json.dumps({"payroll_pk":payroll_obj.pk})
        else:
            json_str = json.dumps({"error":"La peticion no se puede resolver"})
        return HttpResponse(str(json_str), mimetype="application/json")
    else:
        raise Http404


def show_payroll_list(request):
    obj_list = Payroll.objects.all().order_by("-date_added")
    return render_to_response('show_payroll_list.html', locals(), context_instance=RequestContext(request))    

def read_payroll(request, payroll_pk):
    # obj = Payroll.objects.get(pk=payroll_pk)
    # return render_to_response('show_payroll_list.html', locals(), context_instance=RequestContext(request))        
    """Show the list of employees with values of activities, general discounts applied and legal discounts applied."""
    payroll_obj = Payroll.objects.get(pk=payroll_pk)
    payroll_list =[]

    obj_list = MyUser.objects.filter(userprofile__user_type__pk__in=[7,8])

    filling_list = Filling.objects.filter(filling_pro_ord__production_order__payroll=payroll_obj)
    filling_list2 = Filling.objects.filter(filling_pro_ord__production_order__payroll=payroll_obj).aggregate(total=Sum('value'))

    discounts_list = DiscountsApplied.objects.filter(payroll = payroll_obj, is_active=False)
    increases_list = IncreasesApplied.objects.filter(payroll = payroll_obj, is_active=False)

    legal_discounts = LegalDiscounts.objects.filter(is_active=True)

    global_payroll = 0
    for obj in obj_list:
        total_payroll = 0
        #total activities
        activities = filling_list.filter(user=obj, filling_pro_ord__production_order__qualificationproord__status=1, filling_pro_ord__production_order__status=4)
        total_activities = 0
        for a in activities:
            a1 = int(a.filling_pro_ord.production_order.activity.value)
            activity_value = int(a.value) *  a1
            total_activities +=  activity_value
        # total_payroll=total_activities


        #aumentos
        increases = increases_list.filter(employee=obj)
        total_increases = increases.aggregate(t= Sum('value'))
        total_increases_value = total_increases["t"] if total_increases["t"] != None else 0
        # total_payroll = total_payroll+total_increases_value

        total_accrued = total_activities + total_increases_value

        #legal discount
        # if total_activities > (SMMLV*4):
        #     ld = LegalDiscounts.objects.get(pk=2)
        # else:
        #     ld = LegalDiscounts.objects.get(pk=1)
        legal_discount_value = (total_accrued/100)*int(8)
        # total_payroll = total_accrued-legal_discount_value

        #General discount
        discounts = discounts_list.filter(employee=obj)
        total_discounts = discounts.aggregate(t= Sum('value'))
        total_discounts_value = total_discounts["t"] if total_discounts["t"] != None else 0

        total_payroll = total_accrued-total_discounts_value-legal_discount_value
        
        global_payroll += total_payroll

        #payroll
        payroll_list.append({"user": obj,
                             "activities": activities,
                             "total_activities": total_activities,
                             "discounts": discounts,
                             "total_discounts": total_discounts_value,
                             "increases": increases,
                             "total_increases": total_increases_value,
                             "total_payroll": total_payroll,
                             "legal_discount_type": "Seguridad social 8%",  #"%s %s%%"%(ld.name, ld.value),
                             "legal_discount_value": legal_discount_value,
                             "total_accrued": total_accrued
                             #"adjust": adjust
                             })
    last_payroll=True
    return render_to_response('payroll.html', locals(), context_instance=RequestContext(request))
