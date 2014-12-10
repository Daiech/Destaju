from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from apps.account.decorators import access_required
import datetime
# from django.utils.translation import activate
# 


from .models import Inventory, ProviderOrder, EmployedOrder, QuantityProviderTool, QuantityEmployedTool
from .forms import ProviderOrderForm, QuantityProviderToolForm, EmployedOrderForm, QuantityEmployedToolForm
from .utils import is_repeated_tool



@login_required()
@access_required("superadmin", "admin", "storer")
def list_inventory(request):
    list_inventory = Inventory.objects.get_all_active()
    return render_to_response('inventory.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "storer")
def list_provider_order(request):
    list_provider_order = ProviderOrder.objects.get_all_active().order_by('-date_added')
    if request.method == 'POST':    
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm)
        formset =  QuantityProviderToolFormSet(request.POST)
        form = ProviderOrderForm(request.POST) 
        if formset.is_valid():
            
            if not is_repeated_tool(formset):
                object_list = formset.save(commit=False)
                
                if form.is_valid() and len(object_list) > 0:
                    provider_order_obj = form.save(commit=False)
                    provider_order_obj.user_generator = request.user
                    provider_order_obj.status_order = 'Waiting'

                    form.save()

                    for obj in object_list:
                        obj.provider_order = provider_order_obj
                    formset.save()
                    return HttpResponseRedirect(reverse('list_provider_order'))

                else:
                    show_form = True
                    if len(object_list) == 0:
                        error = "Debes llenar por lo menos un item"
            else:
                show_form = True
                error = "No puede haber items repetidos en la orden"
        else:
            show_form = True
            form = ProviderOrderForm(request.POST)
    else:
        form = ProviderOrderForm()
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm, extra=5)
        qs = QuantityProviderTool.objects.none()
        formset =  QuantityProviderToolFormSet(queryset = qs) # initial=responsible,
        provider_order_id = request.GET.get('provider_order_id')
        if provider_order_id:
            provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
            show_provider_order_modal = True

    return render_to_response('provider_order.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "storer")
def approve_provider_order(request):
    provider_order_id = request.GET.get('provider_order_id')
    if provider_order_id:
        provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
        if provider_order_obj.status_order == "Waiting":
            quantityprovidertool_list = provider_order_obj.quantityprovidertool_provider_order.all()
            for quantityprovidertool_obj in quantityprovidertool_list:
                inventory_obj = Inventory.objects.get_or_none(id=quantityprovidertool_obj.tool.id)
                if not inventory_obj:
                    inventory_obj = Inventory.objects.create(tool=quantityprovidertool_obj.tool, quantity=0)
                inventory_obj.quantity = inventory_obj.quantity+quantityprovidertool_obj.quantity 
                inventory_obj.save()
            provider_order_obj.status_order = "Approved"
            provider_order_obj.user_approver = request.user
            provider_order_obj.date_approved = datetime.datetime.now()
            provider_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_provider_order'))


@login_required()
@access_required("superadmin", "admin", "storer")
def reject_provider_order(request):
    provider_order_id = request.GET.get('provider_order_id')
    if provider_order_id:
        provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
        if provider_order_obj.status_order == "Waiting":
            provider_order_obj.status_order = "Not_Approved"
            provider_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_provider_order'))


@login_required()
@access_required("superadmin", "admin", "storer")
def list_item_history(request):
    
    tool_id = request.GET.get('tool_id')
    if not tool_id:
        return HttpResponseRedirect(reverse('list_inventory'))

    inventory_obj = Inventory.objects.get_or_none(tool__id = tool_id)
    if not inventory_obj:
        return HttpResponseRedirect(reverse('list_inventory'))
    
    # print inventory_obj

    quantityprovidertool_list = QuantityProviderTool.objects.filter(tool__id=tool_id, provider_order__status_order="Approved")
    quantityemployedtool_list = QuantityEmployedTool.objects.filter(tool__id=tool_id, employed_order__status_order="Approved") #provider_order__status_order="Approved"
    # print quantityprovidertool_list
    return render_to_response('item_history.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "storer")
def list_employed_order(request):
    
    if request.method == 'POST':
        QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm)
        formset =  QuantityEmployedToolFormSet(request.POST)
        form = EmployedOrderForm(request.POST) 
        
        if form.is_valid() and len(formset.forms) > 0:
            employed_order_obj = form.save(commit=False)
            employed_order_obj.user_generator = request.user
            employed_order_obj.status_order = 'Waiting'
            
            for q_form in formset.forms:
                q_form.add_employed_order(employed_order_obj)


            if formset.is_valid():

                if not is_repeated_tool(formset):
                    form.save()
                    object_list = formset.save(commit=False)
                    for obj in object_list:
                        obj.employed_order = employed_order_obj

                    formset.save()
                    return HttpResponseRedirect(reverse('list_employed_order'))
                else:
                    show_form = True
                    error = "No puede haber items repetidos en la orden"
            else:
                show_form = True
                form = EmployedOrderForm(request.POST)
        else:
            show_form = True
            if len(formset.forms) == 0:
                error = "Debes llenar por lo menos un item"

    else:
        employed_order_id = request.GET.get('employed_order_id')
        if employed_order_id:
            employed_order_obj = EmployedOrder.objects.get(id=employed_order_id)
            show_employed_order_modal = True

        form = EmployedOrderForm()
        QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm, extra=5)
        qs = QuantityEmployedTool.objects.none()
        formset =  QuantityEmployedToolFormSet(queryset = qs) # initial=responsible,
        employed_order_id = request.GET.get('employed_order_id')
        


    error_url = request.GET.get('error')
    if error_url:
        if error_url == "1":
            error = "No hay suficientes items en el almacen para satisfacer la orden de salida"
        if error_url == "2":
            error = "Se esta intentando solicitar un item que no esta registrado en el inventario"
    list_employed_order = EmployedOrder.objects.get_all_active().order_by('-date_added')
    return render_to_response('employed_order.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "storer")
def approve_employed_order(request):
    employed_order_id = request.GET.get('employed_order_id')
    # type_order = request.GET.get('type_order')
    if employed_order_id:
        employed_order_obj = EmployedOrder.objects.get(id=employed_order_id)
        if employed_order_obj.status_order == "Waiting":
            quantityemployedtool_list = employed_order_obj.quantityemployedtool_employed_order.all()
            for quantityemployedtool_obj in quantityemployedtool_list:
                inventory_obj = Inventory.objects.get_or_none(id=quantityemployedtool_obj.tool.id)
                if not inventory_obj:
                    return HttpResponseRedirect(reverse('list_employed_order')+'?error=2')
                if employed_order_obj.type_order != "Recovery"  and inventory_obj.quantity < quantityemployedtool_obj.quantity:
                    return HttpResponseRedirect(reverse('list_employed_order')+'?error=1')
                
            for quantityemployedtool_obj in quantityemployedtool_list:
                inventory_obj = Inventory.objects.get_or_none(id=quantityemployedtool_obj.tool.id)
                if employed_order_obj.type_order == "Recovery":
                    inventory_obj.quantity = inventory_obj.quantity+quantityemployedtool_obj.quantity 
                else:
                    inventory_obj.quantity = inventory_obj.quantity-quantityemployedtool_obj.quantity 
                inventory_obj.save()
            employed_order_obj.status_order = "Approved"
            employed_order_obj.user_approver = request.user
            employed_order_obj.date_approved = datetime.datetime.now()
            employed_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_employed_order'))


@login_required()
@access_required("superadmin", "admin", "storer")
def reject_employed_order(request):
    employed_order_id = request.GET.get('employed_order_id')
    if employed_order_id:
        employed_order_obj = EmployedOrder.objects.get(id=employed_order_id)
        if employed_order_obj.status_order == "Waiting":
            employed_order_obj.status_order = "Not_Approved"
            employed_order_obj.user_approver = request.user
            employed_order_obj.date_approved = datetime.datetime.now()
            employed_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_employed_order'))