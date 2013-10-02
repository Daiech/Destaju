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

@login_required()
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
def update_production_order(request, id_production_order):
    """Manage tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
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
    object_list = ProductionOrder.objects.get_all_active()
    return render_to_response("production_order.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_production_order(request, id_production_order):
    """Logical deletion of tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(create_production_order))








