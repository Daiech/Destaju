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
    # activate('ES')
    list_provider_order = ProviderOrder.objects.get_all_active()
    if request.method == 'POST':    
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm)
        formset =  QuantityProviderToolFormSet(request.POST)
        if formset.is_valid():
            # filling_pro_ord_obj = FillingProOrd(user=request.user, production_order=po)
            # filling_pro_ord_obj.save()
            form = ProviderOrderForm(request.POST) #instance=filling_pro_ord_obj
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
                print "FORM NO VALIDO"
                show_form = True
        else:
            print "FORMULARIO formset NO VALIDO"
            show_form = True
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
        QuantityProviderToolFormSet = modelformset_factory(QuantityProviderTool, form=QuantityProviderToolForm, extra=2)
        qs = QuantityProviderTool.objects.none()
        formset =  QuantityProviderToolFormSet(queryset = qs) # initial=responsible,
        # elif po.status == 2:
        #     form = FillingProOrdForm(instance = po.fillingproord)
        #     FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=0)
        #     qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
        #     formset =  FillingFormSet(queryset = qs)
        # else:
        #     return HttpResponseRedirect(reverse(filling_pro_ord))
        provider_order_id = request.GET.get('provider_order_id')
        if provider_order_id:
            provider_order_obj = ProviderOrder.objects.get(id=provider_order_id)
            print provider_order_obj
            show_provider_order_modal = True




    return render_to_response('provider_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_employed_order(request):
    list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('employed_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_item_history(request):
    # list_employed_order = EmployedOrder.objects.get_all_active()
    return render_to_response('item_history.html', locals(), context_instance=RequestContext(request))
