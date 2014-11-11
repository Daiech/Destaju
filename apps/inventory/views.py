from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.utils.translation import activate


from .models import Inventory, ProviderOrder, EmployedOrder, QuantityProviderTool
from .forms import ProviderOrderForm, QuantityProviderToolForm



@login_required()
def list_inventory(request):
    list_inventory = Inventory.objects.get_all_active()
    return render_to_response('inventory.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_provider_order(request):
    list_provider_order = ProviderOrder.objects.get_all_active().order_by('-date_added')
    if request.method == 'POST':    
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm)
        formset =  QuantityProviderToolFormSet(request.POST)
        if formset.is_valid():
            form = ProviderOrderForm(request.POST) 
            if form.is_valid():
                provider_order_obj = form.save(commit=False)
                provider_order_obj.user_generator = request.user
                provider_order_obj.status_order = 'Waiting'
                form.save()

                object_list = formset.save(commit=False)
                for obj in object_list:
                    obj.provider_order = provider_order_obj
                formset.save()
                return HttpResponseRedirect(reverse('list_provider_order'))
                
            else:
                show_form = True
        else:
            show_form = True
            form = ProviderOrderForm(request.POST)
    else:
        form = ProviderOrderForm()
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm, extra=2)
        qs = QuantityProviderTool.objects.none()
        formset =  QuantityProviderToolFormSet(queryset = qs) # initial=responsible,
        provider_order_id = request.GET.get('provider_order_id')
        if provider_order_id:
            provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
            show_provider_order_modal = True

    return render_to_response('provider_order.html', locals(), context_instance=RequestContext(request))


@login_required()
def approve_provider_order(request):
    provider_order_id = request.GET.get('provider_order_id')
    print "PROVIDER ORDER ID", provider_order_id
    if provider_order_id:
        provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
        print "PROVIDER ORDER OBJ", provider_order_obj
        if provider_order_obj.status_order == "Waiting":
            print "TRUE"
            provider_order_obj.status_order = "Approved"

            quantityprovidertool_list = provider_order_obj.quantityprovidertool_provider_order.all()
            for quantityprovidertool_obj in quantityprovidertool_list:
                print " herramienta"
                print quantityprovidertool_obj.id, quantityprovidertool_obj.tool, quantityprovidertool_obj.quantity
                inventory_obj = Inventory.objects.get_or_none(id=quantityprovidertool_obj.tool.id)
                if not inventory_obj:
                    inventory_obj = Inventory.objects.create(tool=quantityprovidertool_obj.tool, quantity=0)

                print inventory_obj.id, inventory_obj.tool, inventory_obj.quantity
                inventory_obj.quantity = inventory_obj.quantity+quantityprovidertool_obj.quantity 
                inventory_obj.save()
            provider_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_provider_order'))


@login_required()
def reject_provider_order(request):
    provider_order_id = request.GET.get('provider_order_id')
    if provider_order_id:
        provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
        if provider_order_obj.status_order == "Waiting":
            provider_order_obj.status_order = "Not_Approved"
            provider_order_obj.save()
            
    return HttpResponseRedirect(reverse('list_provider_order'))


@login_required()
def list_item_history(request):
    # list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('item_history.html', locals(), context_instance=RequestContext(request))



@login_required()
def list_employed_order(request):
    list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('employed_order.html', locals(), context_instance=RequestContext(request))
