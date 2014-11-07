from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Inventory, ProviderOrder, EmployedOrder


@login_required()
def list_inventory(request):
	list_inventory = Inventory.objects.get_all_active()
	return render_to_response('inventory.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_provider_order(request):
	list_provider_order = ProviderOrder.objects.get_all_active()
	return render_to_response('provider_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_employed_order(request):
	list_employed_order = EmployedOrder.objects.get_all_active()
	return render_to_response('employed_order.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_item_history(request):
	# list_employed_order = EmployedOrder.objects.get_all_active()
	return render_to_response('item_history.html', locals(), context_instance=RequestContext(request))
