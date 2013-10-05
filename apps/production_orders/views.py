# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.production_orders.forms import *
from apps.production_orders.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#from django.core import serializers
#from apps.actions_log.views import save_with_modifications
from apps.process_admin.models import Tools, Places, Activities
from apps.actions_log.views import save_with_modifications
# from django.forms.formsets import modelformset_factory
from django.forms.models import modelformset_factory
from apps.account.decorators import access_required


@login_required()
@access_required("superadmin", "admin", "s1")
def create_production_order(request):
    """Form to generate a production order"""
    if request.method == 'POST':
        form  = ProductionOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            for tool in request.POST.getlist('tools'):
                obj.tools.add(tool)
                
            for user in request.POST.getlist('responsible'):
                obj.responsible.add(user)

            form.save_m2m()

            form = ProductionOrderForm()
            return HttpResponseRedirect(reverse(create_production_order))
        else:
                show_form = True
        if '_createanother' in request.POST:
            show_form = True
    else:
        form  = ProductionOrderForm() 
    form_mode  = "_create"
    object_list = ProductionOrder.objects.get_all_active()
    return render_to_response('production_order.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def update_production_order(request, id_production_order):
    """Manage tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    if obj.status == 1:
        if request.method == "POST":
            form = ProductionOrderForm(request.POST, instance=obj)
            if form.is_valid():
                save_with_modifications(request.user, form, obj, ProductionOrder)
                return HttpResponseRedirect(reverse(create_production_order))
            else:
                show_form = True
        else:
            show_form = True
            form = ProductionOrderForm(instance=obj)
        form_mode = "_update"
    else:
        return HttpResponseRedirect(reverse(create_production_order))
    object_list = ProductionOrder.objects.get_all_active()
    return render_to_response("production_order.html", locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def delete_production_order(request, id_production_order):
    """Logical deletion of tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(create_production_order))


@login_required()
@access_required("superadmin", "admin", "s2")
def filling_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s2")
def filling(request, id_production_order):
    """Form to filling a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 1:
            FillingFormSet = modelformset_factory(Filling, form=FillingForm)
            formset =  FillingFormSet(request.POST)
            if formset.is_valid():
                filling_pro_ord_obj = FillingProOrd(user=request.user, production_order=po)
                filling_pro_ord_obj.save()
                po.status = 2
                po.save()
                object_list = formset.save(commit=False)
                for obj in object_list:
                    obj.filling_pro_ord = filling_pro_ord_obj
                formset.save()
                return HttpResponseRedirect(reverse(filling_pro_ord))
        else:

            qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
            FillingFormSet = modelformset_factory(Filling, form=FillingForm,  extra=0)
            formset =  FillingFormSet(request.POST, queryset=qs)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(reverse(filling_pro_ord))
    else:
        responsible_list = ProductionOrder.objects.get(pk=id_production_order).responsible.all()
        responsible = []
        for user in responsible_list:
            responsible.append({"user":user})
        if po.status == 1:
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=len(responsible))
            qs = Filling.objects.none()
            formset =  FillingFormSet(initial=responsible,queryset = qs)
        elif po.status == 2:
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=0)
            qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
            formset =  FillingFormSet(queryset = qs)
        else:
            HttpResponseRedirect(reverse(filling_pro_ord))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
    form_mode = "_update"
    show_form =True
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3])
    return render_to_response('qualification_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification(request, id_production_order):
    """Form to qualify a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 2:
            QualificationsFormSet = modelformset_factory(Qualifications, form=QualificationsForm)
            formset =  QualificationsFormSet(request.POST)
            if formset.is_valid():
                qualification_pro_ord_obj = QualificationProOrd(user=request.user, production_order=po)
                qualification_pro_ord_obj.save()
                po.status = 3
                po.save()
                object_list = formset.save(commit=False)
                for obj in object_list:
                    obj.qualification_pro_ord = qualification_pro_ord_obj
                formset.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        elif po.status == 3:
            qs = Qualifications.objects.filter(qualification_pro_ord=QualificationProOrd.objects.get(production_order=po))
            QualificationsFormSet = modelformset_factory(Qualifications, form=QualificationsForm,  extra=0)
            formset =  QualificationsFormSet(request.POST, queryset=qs)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        else:
            return HttpResponseRedirect(reverse(qualification_pro_ord))
    else:
        responsible_list = ProductionOrder.objects.get(pk=id_production_order).responsible.all()
        responsible = []
        for user in responsible_list:
            responsible.append({"user":user})
        if po.status == 2:
            QualificationsFormSet = modelformset_factory(Qualifications, form=QualificationsForm, extra=len(responsible))
            qs = Qualifications.objects.none()
            formset =  QualificationsFormSet(initial=responsible,queryset = qs)
        elif po.status == 3:
            QualificationsFormSet = modelformset_factory(Qualifications, form=QualificationsForm, extra=0)
            qs = Qualifications.objects.filter(qualification_pro_ord=QualificationProOrd.objects.get(production_order=po))
            formset =  QualificationsFormSet(queryset = qs)
        else:
            HttpResponseRedirect(reverse(qualification_pro_ord))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3])
    form_mode = "_update"
    show_form =True
    return render_to_response('qualification_pro_ord.html', locals(), context_instance=RequestContext(request))




