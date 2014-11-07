from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import modelformset_factory

from .models import Inventory, ProviderOrder, EmployedOrder, QuantityProviderTool
from .forms import ProviderOrderForm, QuantityProviderToolForm



@login_required()
def list_inventory(request):
    list_inventory = Inventory.objects.get_all_active()
    return render_to_response('inventory.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_provider_order(request):
    list_provider_order = ProviderOrder.objects.get_all_active()
    if request.method == 'POST':
    #     if po.status == 1:
		QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm)
		formset =  QuantityProviderToolFormSet(request.POST)
		if formset.is_valid():
		    # filling_pro_ord_obj = FillingProOrd(user=request.user, production_order=po)
		    # filling_pro_ord_obj.save()
		    # form = FillingProOrdForm(request.POST, instance=filling_pro_ord_obj)
		    # if form.is_valid():
		    #     form.save()
		    # po.status = 2
		    # po.save()
		    # object_list = formset.save(commit=False)
		    # for obj in object_list:
		    #     obj.filling_pro_ord = filling_pro_ord_obj
		    # formset.save()
		    # return HttpResponseRedirect(reverse(filling_pro_ord))
		    print "FORMULARIO formset  VALIDO"
		    print formset
		else:
		    # formset = QuantityProviderToolForm(request.POST)
		    form = ProviderOrderForm(request.POST)
    #     else:
    #         form = FillingProOrdForm(request.POST, instance = po.fillingproord)
    #         if form.is_valid():
    #                 form.save()
    #         qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
    #         FillingFormSet = modelformset_factory(Filling, form=FillingForm,  extra=0)
    #         formset =  FillingFormSet(request.POST, queryset=qs)
    #         if formset.is_valid():
    #             formset.save()
    else:
        # responsible_list = ProductionOrder.objects.get(pk=id_production_order).responsible.all()
        # responsible = []
        # for user in responsible_list:
        #     responsible.append({"user":user})
        # if po.status == 1:
		form = ProviderOrderForm()
		QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm, extra=3)
		qs = QuantityProviderTool.objects.none()
		formset =  QuantityProviderToolFormSet(queryset = qs) # initial=responsible,
        # elif po.status == 2:
        #     form = FillingProOrdForm(instance = po.fillingproord)
        #     FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=0)
        #     qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
        #     formset =  FillingFormSet(queryset = qs)
        # else:
        #     return HttpResponseRedirect(reverse(filling_pro_ord))



    return render_to_response('provider_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_employed_order(request):
    list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('employed_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_item_history(request):
    # list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('item_history.html', locals(), context_instance=RequestContext(request))
