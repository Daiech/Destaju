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
from django.db.models import Max
from django.utils import simplejson as json

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
            if '_createanother' in request.POST:
                show_form = True
            else:
                return HttpResponseRedirect(reverse(create_production_order))
        else:
            show_form = True
#        if '_createanother' in request.POST:
#            show_form = True
    else:
        form  = ProductionOrderForm() 
    form_mode  = "_create"
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
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
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
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
                form = FillingProOrdForm(request.POST, instance=filling_pro_ord_obj)
                if form.is_valid():
                    form.save()
                po.status = 2
                po.save()
                object_list = formset.save(commit=False)
                for obj in object_list:
                    obj.filling_pro_ord = filling_pro_ord_obj
                formset.save()
                return HttpResponseRedirect(reverse(filling_pro_ord))
            else:
                form = FillingProOrdForm(request.POST)
        else:
            form = FillingProOrdForm(request.POST, instance = po.fillingproord)
            if form.is_valid():
                    form.save()
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
            form = FillingProOrdForm()
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=len(responsible))
            qs = Filling.objects.none()
            formset =  FillingFormSet(initial=responsible,queryset = qs)
        elif po.status == 2:
            form = FillingProOrdForm(instance = po.fillingproord)
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=0)
            qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
            formset =  FillingFormSet(queryset = qs)
        else:
            return HttpResponseRedirect(reverse(filling_pro_ord))
        
        
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    form_mode = "_update"
    show_form =True
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('qualification_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification(request, id_production_order):
    """Form to qualify a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 2:
            form =  QualificationsForm(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.user=request.user 
                obj.production_order=po
                obj.save()
                po.status = 3
                po.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        elif po.status == 3:
            form =  QualificationsForm(request.POST, instance= po.qualificationproord)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        else:
            return HttpResponseRedirect(reverse(qualification_pro_ord))
    else:
        if po.status == 2:
            form =  QualificationsForm()
        elif po.status == 3:
            form =  QualificationsForm(instance = po.qualificationproord)
        else:
            return HttpResponseRedirect(reverse(qualification_pro_ord))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    #    form_mode = "_create"
    show_form =True
    return render_to_response('qualification_form.html', locals(), context_instance=RequestContext(request))


def list_production_orders(request):
    if request.method == 'POST':
        form = ListProductionOrderForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            type_date = form.cleaned_data['type_date']
            if type_date == 'added':
                object_list = ProductionOrder.objects.filter(date_added__gt = date_from).filter(date_added__lt = date_to)
            elif type_date == 'modified':
                object_list = ProductionOrder.objects.filter(date_modified__gt = date_from).filter(date_modified__lt = date_to)
            elif type_date == 'filling':
                object_list = ProductionOrder.objects.filter(fillingproord__date_modified__gt = date_from).filter(fillingproord__date_modified__lt = date_to)
            else:
                print "Error"
    else:
        form = ListProductionOrderForm()
    return render_to_response('list_production_orders.html', locals(), context_instance=RequestContext(request))

def show_production_order_ajax(request, id_production_order):
#    if request.is_ajax():
    if request.method == "GET":
        obj = get_object_or_404(ProductionOrder, pk=id_production_order)
        response = {"obj":obj}
    else:
        response = u"Peticion denegada"
    return HttpResponse(json.dumps(response), mimetype="application/json")
#    else:
#        return "Ha ocurrido un error"
        

























